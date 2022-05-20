from dataclasses import dataclass
from typing import Any

import numpy as np

@dataclass
class Column:
    """Column class with methods to help DataClass implementation

    TODO: add bool params checks
    """
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
