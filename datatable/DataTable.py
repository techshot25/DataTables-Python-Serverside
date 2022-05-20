
from dataclasses import dataclass
import re
from typing import Any

import numpy as np


@dataclass
class Column:
    # TODO: add search
    data: list
    name: str
    orderable: bool = True
    searchable: bool = True
    search: Any = None
    def __post_init__(self):
        self.data = np.array(self.data)

    def argsort(self, dir="asc"):
        if dir == "asc":
            return np.argsort(self.data)
        else:
            return np.argsort(self.data)[::-1]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return list(self.data)[key]

    def __iter__(self):
        return iter(self.data)

class DataTable:
    def __init__(self, raw_data):
        assert len(set(len(row) for row in raw_data.values())) == 1, \
            "Columns must have equal sizes"

        self._dict = raw_data
        self._list = self.transpose(raw_data)

    @staticmethod
    def transpose(data):
        if isinstance(data, dict):
            keys = data.keys()
            return [{key: val for key, val in zip(keys, row)} for row in zip(*data.values())]
        if isinstance(data, list):
            if isinstance(data[0], Column):
                names = tuple(col.name for col in data)
            elif isinstance(data[0], dict):
                names = data[0].keys()
            else:
                raise ValueError("Not a recognized data type")
            return [dict(zip(names, row)) for row in zip(*data)]
        raise ValueError("Not a recognized data type")

    @staticmethod
    def sort(columns, idx, dir="asc"):
        order_keys = columns[idx].argsort(dir=dir)
        col_space = len(columns)        
        for i in range(col_space):
            columns[i].data = columns[i].data[order_keys]

    def search(self, columns, value, regex=False):
        if len(value) == 0:
            return columns
        row_wise = self.transpose(columns)
        if regex:
            pattern = re.compile(value)
            return [row for row in row_wise
                    if any(pattern.match(str(x)) for x in row.values())]
        return [row for row in row_wise
                if any(value in str(x) for x in row.values())]

    def render(self, data, start, length):
        if isinstance(data[0], Column):
            view = {col.name: col[start:start+length] for col in data}
            return self.transpose(view)
        elif isinstance(data[0], dict):
            return data

    def __call__(self, config: dict):
        draw = config["draw"]
        columns = [Column(
                data=self._dict[col['data']],
                name=col['data'],
                orderable=col['orderable'],
                searchable=col['searchable']
            ) for col in config['columns']]

        # first filtering step
        order = config['order'][0]
        self.sort(columns, order['column'], order['dir'])

        if columns:
            search = config['search']
            columns = self.search(columns, search['value'], search['regex'])
        
        start = config['start']
        length = config['length']

        return {
            "data": self.render(columns, start, length),
            "draw": draw,
            "recordsTotal": len(self._list),
            "recordsFiltered": len(columns[0]) if len(columns) > 0 else 0
        }

