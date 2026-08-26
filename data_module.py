import os
import pandas as pd
import xarray as xr
import numpy as np


# ==================================================
# EXISTING DATAFRAME FUNCTIONS
# ==================================================

def load_data():
    data = {
        "latitude": [-70.5, -71.2],
        "longitude": [20.3, 21.8],
        "iceberg_id": ["IB001", "IB002"],
        "sea_ice_concentration": [85, 72]
    }

    return pd.DataFrame(data)


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
# ANTARCTIC NETCDF DATA FUNCTIONS
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

    # Check required variables
    for variable in required_variables:
        if variable not in ds.variables:
            raise ValueError(
                f"Missing required variable: {variable}"
            )

    # Check sea-ice dimensions
    sea_ice = ds["cdr_seaice_conc"]

    expected_dimensions = {"time", "x", "y"}

    if not expected_dimensions.issubset(
        set(sea_ice.dims)
    ):
        raise ValueError(
            f"Unexpected dimensions: {sea_ice.dims}"
        )

    # Get actual numeric values
    values = sea_ice.values

    # Remove NaN values only for range checking
    valid_values = values[
        ~np.isnan(values)
    ]

    # Check sea-ice concentration range
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

    Missing values are preserved because
    they may represent unavailable observations.
    """

    ds = ds.copy()

    sea_ice = ds["cdr_seaice_conc"]

    # Keep valid values and preserve NaN values
    ds["cdr_seaice_conc"] = sea_ice.where(
        sea_ice >= 0
    )

    return ds


def preprocess_netcdf_data(ds):
    """
    Prepare NetCDF dataset for other modules.
    """

    ds = ds.copy()

    # Convert concentration to float32
    ds["cdr_seaice_conc"] = ds[
        "cdr_seaice_conc"
    ].astype("float32")

    return ds


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