import os
import pandas as pd
import xarray as xr
import numpy as np
from pyproj import Transformer


# ==================================================
# DATAFRAME FUNCTIONS
# ==================================================

def load_data():
    data = {
        "latitude": [-70.5, -71.2],
        "longitude": [20.3, 21.8],
        "iceberg_id": ["IB001", "IB002"],
        "sea_ice_concentration": [85, 72]
    }

    return pd.DataFrame(data)

def data_quality_report(df):
    """
    Generate a detailed data quality report.
    """

    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "missing_by_column": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum())
    }

    if "latitude" in df.columns:
        report["latitude_range"] = (
            float(df["latitude"].min()),
            float(df["latitude"].max())
        )

    if "longitude" in df.columns:
        report["longitude_range"] = (
            float(df["longitude"].min()),
            float(df["longitude"].max())
        )

    if "sea_ice_concentration" in df.columns:
        report["sea_ice_concentration_range"] = (
            float(df["sea_ice_concentration"].min()),
            float(df["sea_ice_concentration"].max())
        )

    return report

def load_processed_data(file_path):
    """
    Load processed Antarctic data from CSV.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Processed data file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def validate_data(df):
    required_columns = [
        "latitude",
        "longitude",
        "iceberg_id",
        "sea_ice_concentration"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if df["latitude"].isnull().any():
        raise ValueError("Latitude contains missing values")

    if df["longitude"].isnull().any():
        raise ValueError("Longitude contains missing values")

    if df["sea_ice_concentration"].isnull().any():
        raise ValueError("Sea ice concentration contains missing values")

    if not df["latitude"].between(-90, 90).all():
        raise ValueError("Invalid latitude value")

    if not df["longitude"].between(-180, 180).all():
        raise ValueError("Invalid longitude value")

    if not df["sea_ice_concentration"].between(0, 100).all():
        raise ValueError("Invalid sea ice concentration")

    return True


def clean_data(df):
    df = df.copy()

    df = df.drop_duplicates()

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    df["sea_ice_concentration"] = pd.to_numeric(
        df["sea_ice_concentration"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "latitude",
            "longitude",
            "iceberg_id",
            "sea_ice_concentration"
        ]
    )

    return df.reset_index(drop=True)


def preprocess_data(df):
    df = df.copy()

    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["sea_ice_concentration"] = df[
        "sea_ice_concentration"
    ].astype(float)

    df["iceberg_id"] = df["iceberg_id"].astype(str)

    return df


# ==================================================
# NETCDF FUNCTIONS
# ==================================================

def load_netcdf_data(file_path):
    """
    Load Antarctic sea-ice NetCDF dataset.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"NetCDF file not found: {file_path}"
        )

    ds = xr.open_dataset(
        file_path,
        engine="netcdf4"
    )

    return ds


def validate_netcdf_data(ds):
    """
    Validate Antarctic sea-ice NetCDF dataset.
    """

    required_variables = [
        "cdr_seaice_conc",
        "cdr_seaice_conc_stdev",
        "cdr_seaice_conc_qa_flag",
        "cdr_seaice_conc_interp_spatial_flag",
        "cdr_seaice_conc_interp_temporal_flag"
    ]

    for variable in required_variables:
        if variable not in ds.variables:
            raise ValueError(
                f"Missing required variable: {variable}"
            )

    sea_ice = ds["cdr_seaice_conc"]

    expected_dimensions = {
        "time",
        "x",
        "y"
    }

    if not expected_dimensions.issubset(
        set(sea_ice.dims)
    ):
        raise ValueError(
            f"Unexpected dimensions: {sea_ice.dims}"
        )

    values = sea_ice.values

    valid_values = values[
        ~np.isnan(values)
    ]

    if valid_values.size > 0:

        if valid_values.min() < 0:
            raise ValueError(
                "Sea-ice concentration contains values below 0"
            )

        if valid_values.max() > 1:
            raise ValueError(
                "Sea-ice concentration contains values above 1"
            )

    return True


def clean_netcdf_data(ds):
    """
    Clean Antarctic NetCDF dataset.

    Missing values are preserved.
    """

    ds = ds.copy()

    sea_ice = ds["cdr_seaice_conc"]

    ds["cdr_seaice_conc"] = sea_ice.where(
        sea_ice >= 0
    )

    return ds


def preprocess_netcdf_data(ds):
    """
    Prepare NetCDF dataset for downstream modules.
    """

    ds = ds.copy()

    ds["cdr_seaice_conc"] = ds[
        "cdr_seaice_conc"
    ].astype("float32")

    return ds


# ==================================================
# LATITUDE / LONGITUDE CONVERSION
# ==================================================

def add_latitude_longitude(ds):
    """
    Convert Antarctic Polar Stereographic coordinates
    from EPSG:3412 to latitude/longitude EPSG:4326.
    """

    transformer = Transformer.from_crs(
        "EPSG:3412",
        "EPSG:4326",
        always_xy=True
    )

    # Original x and y coordinates
    x = ds["x"].values
    y = ds["y"].values

    # Create complete 2D grid
    x_grid, y_grid = np.meshgrid(
        x,
        y
    )

    # Convert the complete grid
    lon, lat = transformer.transform(
        x_grid,
        y_grid
    )

    ds = ds.copy()

    # Add 2D longitude
    ds["longitude"] = (
        ("y", "x"),
        lon
    )

    # Add 2D latitude
    ds["latitude"] = (
        ("y", "x"),
        lat
    )

    ds["longitude"].attrs = {
        "units": "degrees_east",
        "long_name": "Longitude"
    }

    ds["latitude"].attrs = {
        "units": "degrees_north",
        "long_name": "Latitude"
    }

    return ds


# ==================================================
# SAVE NETCDF
# ==================================================

def save_netcdf_data(ds, output_path):
    """
    Save processed NetCDF dataset.
    """

    output_directory = os.path.dirname(
        output_path
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    ds.to_netcdf(
        output_path,
        engine="netcdf4"
    )

    return output_path
def export_netcdf_to_csv(ds, output_path):
    """
    Export Antarctic sea-ice NetCDF data to CSV format.

    Each row represents one grid cell.
    """

    df = ds.to_dataframe().reset_index()

    column_mapping = {
        "cdr_seaice_conc": "sea_ice_concentration",
        "cdr_seaice_conc_stdev": "sea_ice_stdev",
        "cdr_seaice_conc_qa_flag": "qa_flag",
        "cdr_seaice_conc_interp_spatial_flag":
            "spatial_interpolation_flag",
        "cdr_seaice_conc_interp_temporal_flag":
            "temporal_interpolation_flag"
    }

    df = df.rename(
        columns=column_mapping
    )

    required_columns = [
        "time",
        "latitude",
        "longitude",
        "sea_ice_concentration",
        "sea_ice_stdev",
        "qa_flag",
        "spatial_interpolation_flag",
        "temporal_interpolation_flag"
    ]

    df = df[
        [
            column
            for column in required_columns
            if column in df.columns
        ]
    ]

    output_directory = os.path.dirname(
        output_path
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    df.to_csv(
        output_path,
        index=False
    )

    return output_path

def run_data_pipeline(input_path, output_path):
    """
    Run the complete Antarctic sea-ice data processing pipeline.

    Pipeline:
    Load → Validate → Clean → Preprocess →
    Add Latitude/Longitude → Export CSV
    """

    ds = load_netcdf_data(input_path)

    validate_netcdf_data(ds)

    ds = clean_netcdf_data(ds)

    ds = preprocess_netcdf_data(ds)

    ds = add_latitude_longitude(ds)

    export_netcdf_to_csv(ds, output_path)

    return output_path