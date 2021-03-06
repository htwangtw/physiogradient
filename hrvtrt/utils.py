import warnings
import re
import json

import pandas as pd


def read_json(json_path):
    """Read json file."""
    with open(json_path, "r") as f:
        meta = json.load(f)
    return meta


def read_tsv(filename, **kargs):
    """Read tsv file, allow pandas.read_csv in kargs."""
    if kargs.get("sep", False):
        raise Exception("There's not need to provide input for `sep`.")

    df = pd.read_csv(filename, sep="\t", **kargs)
    return _check_tsv(df)


def _check_tsv(df):
    """Check if file is tsv."""
    if df.empty is True:
        raise ValueError("File is empty or not a tab separated file.")
    elif "," in df.columns[0]:
        warnings.warn(
            "File is might not be a tab separated file, please check input"
        )
        return df
    else:
        return df


def parse_bids_subject(filename):
    """Get subject and session information form a BIDS filename."""
    matching = re.match("sub-([A-Za-z0-9]*)_ses-([A-Z]*)", filename)
    if matching:
        return matching.group(1), matching.group(2)
    else:
        raise ValueError("Invalid file name. Is the input in BIDS?")
