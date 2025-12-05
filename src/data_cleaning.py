"""
data_cleaning.py

Purpose:
    This script loads a raw sales dataset, applies a series of data
    cleaning steps, and saves a cleaned version that is ready for
    basic analysis. It demonstrates common cleaning tasks such as
    standardizing column names, trimming whitespace, handling missing
    values, and removing clearly invalid rows.
"""

import os
from typing import List

import pandas as pd


# This function loads the raw CSV file into a pandas DataFrame so that
# we can work with the sales data in memory instead of editing the file by hand.
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the raw sales data from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the raw sales data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    df = pd.read_csv(file_path)
    return df


# This function standardizes column names by lowercasing, removing extra
# whitespace, and replacing spaces with underscores. That makes it easier
# to reference columns consistently in Python code.
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names (strip, lowercase, replace spaces with underscores).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with original column names.

    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned column names.
    """
    df = df.copy()
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]
    return df


# This function trims leading and trailing whitespace from all string (object)
# columns so that product names, categories, and other text fields are consistent.
def strip_whitespace_from_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip leading/trailing whitespace from all string columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame that may contain extra spaces in text fields.

    Returns
    -------
    pd.DataFrame
        DataFrame with whitespace removed from string columns.
    """
    df = df.copy()

    string_columns: List[str] = df.select_dtypes(include=["object"]).columns.tolist()

    for col in string_columns:
        df[col] = df[col].astype("string").str.strip()

    return df


# This function handles missing values in the price and quantity columns.
# In this implementation we drop rows where either value is missing so that
# we do not keep transactions with incomplete numeric information.
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values for price and quantity.

    Strategy:
        - Drop rows where price or quantity is NaN, because we cannot
          compute sales correctly without both values.

    Raises
    ------
    KeyError
        If the expected 'price' or 'quantity' columns are not present.
    """
    df = df.copy()

    required_columns = ["price", "quantity"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(
                f"Expected column '{col}' not found in DataFrame. "
                "Check the raw CSV headers and the column cleaning step."
            )

    df = df.dropna(subset=required_columns)

    return df


# This function removes clearly invalid rows, such as negative prices or
# negative quantities, which are almost always data entry errors in a sales dataset.
def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with invalid numeric values (negative price or quantity).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame that may contain invalid numeric values.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame containing only valid rows.
    """
    df = df.copy()

    required_columns = ["price", "quantity"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(
                f"Expected column '{col}' not found in DataFrame. "
                "Check the raw CSV headers and the column cleaning step."
            )

    # Keep only rows with non-negative price and quantity
    df = df[(df["price"] >= 0) & (df["quantity"] >= 0)]

    return df


if __name__ == "__main__":
    # Define input and output paths relative to the project root.
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    # Ensure the processed directory exists before saving.
    processed_dir = os.path.dirname(cleaned_path)
    os.makedirs(processed_dir, exist_ok=True)

    # 1. Load raw data from CSV
    # We load the raw file into a DataFrame so that we can apply
    # all subsequent cleaning steps in Python instead of editing
    # the CSV manually.
    df_raw = load_data(raw_path)

    # 2. Standardize column names
    # Clean, standardized column names (lowercase, underscores)
    # make the dataset easier to use in Python and reduce typos.
    df_clean = clean_column_names(df_raw)

    # 3. Strip whitespace from text columns
    # We remove leading/trailing spaces in text fields so that
    # product names and categories are consistent (e.g., "Shoes"
    # and "Shoes " are treated the
