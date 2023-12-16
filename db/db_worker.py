import os

import pandas as pd


class DBWorkerException(Exception):
    pass


class DBWorker:
    """ Прденазначен для RO бд в виде csv """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def check_path(self) -> bool:
        return os.path.exists(self.csv_path)

    def get_data(self, sep: str = ';') -> list[dict]:
        if not self.check_path():
            raise DBWorkerException('Not found CSV file')

        return pd.read_csv(self.csv_path, sep=sep).to_dict(orient='records')

    @staticmethod
    def merge_other_data(current_data: list[dict], other_data: list[dict], current_pk: str, other_pk: str) -> list[dict]:
        """
            Current Data[current_pk] <==== Other data[other_pk]
        """

        for i, c_data in enumerate(current_data):
            for j, o_data in enumerate(other_data):
                if c_data.get(current_pk) == o_data.get(other_pk):
                    current_data[i][current_pk] = other_data[j]

        return current_data
