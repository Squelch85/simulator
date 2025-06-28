"""Utility functions and column definitions for managing enhancement logs."""

from __future__ import annotations

import pandas as pd
from pandas import DataFrame
from typing import Optional

# Column rules for item inventory
ITEM_COLUMNS = [
    "item_id",       # unique identifier per item
    "item_type",     # e.g., '무기', '방어구'
    "safe_level",    # safe enhancement level
    "current_level", # current enhancement level
    "destroyed"      # bool, whether the item is destroyed
]

# Column rules for aggregated result summary
SUMMARY_COLUMNS = [
    "item_type",  # type of item
    "attempts",   # number of attempts
    "successes",  # number of successes
    "failures",   # number of failures
    "destroyed"   # number of items broken
]

# Column rules for enhancement attempt logs
LOG_COLUMNS = [
    "timestamp",     # attempt time
    "item_id",       # reference to item
    "before_level",  # level before attempt
    "after_level",   # level after attempt
    "increment",     # level increment on success
    "result",        # 'success' or 'fail'
    "destroyed"      # bool, whether item broke
]


def create_item_df() -> DataFrame:
    """Return an empty DataFrame using ITEM_COLUMNS."""
    return pd.DataFrame(columns=ITEM_COLUMNS)


def create_log_df() -> DataFrame:
    """Return an empty DataFrame using LOG_COLUMNS."""
    return pd.DataFrame(columns=LOG_COLUMNS)


def create_summary_df() -> DataFrame:
    """Return an empty DataFrame using SUMMARY_COLUMNS."""
    return pd.DataFrame(columns=SUMMARY_COLUMNS)


def add_item(df: DataFrame, item_type: str, safe_level: int) -> int:
    """Add a new item to df and return its item_id."""
    item_id = int(pd.Timestamp.now().timestamp() * 1_000_000)
    df.loc[len(df)] = {
        "item_id": item_id,
        "item_type": item_type,
        "safe_level": safe_level,
        "current_level": 0,
        "destroyed": False,
    }
    return item_id


def record_attempt(
    log_df: DataFrame,
    item_df: DataFrame,
    item_id: int,
    after_level: int,
    result: str,
    destroyed: bool,
    timestamp: Optional[pd.Timestamp] = None,
) -> None:
    """Record an enhancement attempt in log_df and update item_df."""
    if timestamp is None:
        timestamp = pd.Timestamp.now()

    item_row = item_df[item_df["item_id"] == item_id]
    if item_row.empty:
        raise ValueError("item_id not found")

    before_level = int(item_row.iloc[0]["current_level"])
    increment = max(0, after_level - before_level)

    log_df.loc[len(log_df)] = {
        "timestamp": timestamp,
        "item_id": item_id,
        "before_level": before_level,
        "after_level": after_level,
        "increment": increment,
        "result": result,
        "destroyed": destroyed,
    }

    item_df.loc[item_row.index, "current_level"] = after_level
    if destroyed:
        item_df.loc[item_row.index, "destroyed"] = True
