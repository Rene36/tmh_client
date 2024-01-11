"""Module to change a pandas dataframe"""
# stdlib
import logging
from typing import Union

# third party
import pandas as pd


class ProcessData:
    """
    Functions to clean and pre-process a given
    pandas dataframe for further usage.
    """
    def __init__(self,
                 df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df

    def clean(self):
        """
        Summary of internal functions to pre-process a pandas dataframe
        """
        self._col_to_datetime(col_name=["start_curtailment",
                                        "end_curtailment"])
        self._sort_by_column(col_name="start_curtailment")
        self._calc_cumsum(col_name="energy")

    def get_data(self) -> pd.DataFrame:
        """
        Getter fucntion return pandas dataframe class object

        :return: pandas dataframe,
        """
        return self.df

    def _col_to_datetime(self,
                         col_name: Union[str, list],
                         timestamp_format: str="%Y-%m-%d %H:%M:%S") -> None:
        if isinstance(col_name, str) and col_name in self.df.columns:
            self.df[col_name] = pd.to_datetime(self.df[col_name],
                                               format=timestamp_format)
        elif all(e in list(self.df.columns) for e in col_name):
            for c in col_name:
                self.df[c] = pd.to_datetime(self.df[c],
                                            format=timestamp_format)
        else:
            logging.error("Column %s not in dataframe", col_name)
            raise KeyError(f"Column {col_name} not in dataframe")

    def _sort_by_column(self,
                        col_name: str) -> None:
        self.df.sort_values(by=col_name, ascending=True, inplace=True)

    def _calc_cumsum(self,
                     col_name: str) -> None:
        if col_name in self.df.columns:
            self.df["sum_energy_curtailed"] = self.df[col_name].cumsum()
        else:
            logging.error("Column %s not in dataframe", col_name)
            raise KeyError(f"Column {col_name} not in dataframe")
                                                      