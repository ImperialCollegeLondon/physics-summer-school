"""Convienience wrapper functions for the Physics Summer School."""
import numpy as np
import ipysheet as ips
from ipysheet.sheet import Sheet

EXP_HEADINGS_MAP = {"1": ["Mass", "T (reading %s)"],
                    "2": ["Length", "T (reading %s)"],
                    "3A": ["Periods", "Amplitude (reading %s)"],
                    "3B": ["Time", "Amplitude %s"]}

def _sheet(expno: str, **kwargs) -> Sheet:
    """
    Create blank sheet for data entry.

    Args:
        expno (str): The experiment number

    Returns:
        Sheet: The ipysheet.sheet.Sheet object.
    """
    init_header, other_headers = EXP_HEADINGS_MAP[expno]

    kwargs.pop("column_headers", None)
    column_headers = [init_header]
    column_headers.extend(other_headers % i for i in range(1, kwargs["columns"]))

    sheet1 = ips.sheet(column_headers=column_headers, **kwargs)
    for row in range(sheet1.rows):
        for column in range(sheet1.columns):
            ips.cell(row, column)

    def save(self, filename=f"sheet_exp{expno}.npy"):
        np.save(filename, ips.to_array(self))

    setattr(sheet1.__class__, "to_dataframe", ips.to_dataframe)
    setattr(sheet1.__class__, "to_array", ips.to_array)
    setattr(sheet1.__class__, "save", save)
    return sheet1

def _load(expno: str, filename: str="sheet_exp.npy") -> Sheet:
    """
    Load experiment data.

    Args:
        expno (str): The experiment number
        filename (str, optional): The filename to load from. Defaults to "sheet_exp.npy".

    Returns:
        Sheet: The ipysheet.sheet.Sheet object.
    """
    arr = np.load(filename)
    _, cols = arr.shape

    init_header, other_headers = EXP_HEADINGS_MAP[expno]
    headers = [init_header]
    headers.extend(other_headers % i for i in range(1, cols))

    sheet1 = ips.from_array(arr)
    sheet1.column_headers = headers

    def save(self, filename=f"sheet_exp{expno}.npy"):
        np.save(filename, ips.to_array(self))

    setattr(sheet1.__class__, "to_dataframe", ips.to_dataframe)
    setattr(sheet1.__class__, "to_array", ips.to_array)
    setattr(sheet1.__class__, "save", save)
    return sheet1

# #############################################################################
# Experiment 1.
# #############################################################################
def load_exp1() -> Sheet:
    """
    Load data for experiment 1.

    Returns:
        Sheet: ipysheet.sheet.Sheet object.
    """
    return _load(expno="1", filename="sheet_exp1.npy")

def sheet_exp1(n_masses: int, n_repeats: int) -> Sheet:
    """
    Create blank sheet for experiment 1.

    Args:
        n_masses (int): number of masses
        n_repeats (int): number of repeats

    Raises:
        ValueError: Not enough masses

    Returns:
        Sheet: The ipysheet.sheet.Sheet object
    """
    if n_masses < 3:
        raise ValueError("Please test more than 3 masses")
    return _sheet(expno="1", rows=n_masses, columns=2 + n_repeats)

# #############################################################################
# Experiment 2.
# #############################################################################
def load_exp2() -> Sheet:
    """
    Load data for experiment 2.

    Returns:
        Sheet: ipysheet.sheet.Sheet object.
    """
    return _load(expno="2", filename="sheet_exp2.npy")

def sheet_exp2(n_lengths: int, n_repeats: int) -> Sheet:
    """
    Create blank sheet for experiment 2.

    Args:
        n_lengths (int): number of lengths
        n_repeats (int): number of repeats

    Raises:
        ValueError: Not enough lengths.

    Returns:
        Sheet: the ipysheet.sheet.Sheet object
    """
    if n_lengths < 3:
        raise ValueError("Please test more than 3 lengths")
    return _sheet(expno="2", rows=n_lengths, columns=2 + n_repeats)

# #############################################################################
# Experiment 3A.
# #############################################################################
def load_exp3A() -> Sheet:
    """
    Load data for experiment 3.

    Returns:
        Sheet: ipysheet.sheet.Sheet object.
    """
    return _load(expno="3A", filename="sheet_exp3A.npy")

def sheet_exp3A(n_periods: int, n_repeats: int) -> Sheet:
    """
    Create blank sheet for experiment 3.

    Args:
        n_lengths (int): number of periods
        n_repeats (int): number of repeats

    Raises:
        ValueError: Not enough periods.

    Returns:
        Sheet: the ipysheet.sheet.Sheet object
    """
    if n_periods < 2:
        raise ValueError("Please test more than 2 periods")
    return _sheet(expno="3A", rows=n_periods, columns=2 + n_repeats)

# #############################################################################
# Experiment 3B.
# #############################################################################
def load_exp3B() -> Sheet:
    """
    Load data for experiment 3.

    Returns:
        Sheet: ipysheet.sheet.Sheet object.
    """
    return _load(expno="3B", filename="sheet_exp3B.npy")

def sheet_exp3B(n_readings: int) -> Sheet:
    """
    Create blank sheet for experiment 3.

    Args:
        n_readings (int): number of readings

    Raises:
        ValueError: Not enough periods.

    Returns:
        Sheet: the ipysheet.sheet.Sheet object
    """
    if n_readings < 2:
        raise ValueError("Please test more than 2 readings")
    return _sheet(expno="3B", rows=n_readings, columns=2)

# #############################################################################
# Experiment 3 (generic).
# #############################################################################
def load_sheet(filename: str="sheet_exp3.npy"):
    sheet1 = ips.from_array(np.load(filename))
    def save(self, filename=filename):
        np.save(filename, ips.to_array(self))

    setattr(sheet1.__class__, "to_dataframe", ips.to_dataframe)
    setattr(sheet1.__class__, "to_array", ips.to_array)
    setattr(sheet1.__class__, "save", save)
    return sheet1

def create_sheet(rows: int, columns: int, filename: str="sheet_exp3.npy") -> Sheet:
    sheet1 = ips.sheet(rows=rows, columns=columns)
    def save(self, filename=filename):
        np.save(filename, ips.to_array(self))

    setattr(sheet1.__class__, "to_dataframe", ips.to_dataframe)
    setattr(sheet1.__class__, "to_array", ips.to_array)
    setattr(sheet1.__class__, "save", save)
    return sheet1

__all__ = ("sheet_exp1", "sheet_exp2", "sheet_exp3A", "sheet_exp3B",
           "load_exp1", "load_exp2", "load_exp3A", "load_exp3B",
           "create_sheet", "load_sheet")
