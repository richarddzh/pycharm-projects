from typing import TypeVar
from typing import Generic
from typing import Optional
from typing import List
from typing import Callable


def last_index(a_list, func):
    for i in range(len(a_list) - 1, -1, -1):
        if func(a_list[i]):
            return i
    return -1


T = TypeVar('T')


class Array1D(Generic[T]):
    def __init__(self, size, ctor: Callable[[], T]):
        self.size = size
        self.items = []
        for i in range(0, size):
            self.items.append(ctor())

    def __getitem__(self, item):
        return self.items[item]


class Array2D(Generic[T]):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []  # type: List[T]

    def set(self, y, x, elem: T):
        if y >= self.height:
            self.height = y + 1
        if x >= self.width:
            self.width = x + 1
        while len(self.rows) < self.height:
            self.rows.append([])
        while len(self.rows[y]) < self.width:
            self.rows[y].append(None)
        self.rows[y][x] = elem

    def get(self, y, x) -> Optional[T]:
        if y >= len(self.rows):
            return None
        if x >= len(self.rows[y]):
            return None
        return self.rows[y][x]

    def for_each_not_none(self, action: Callable[[int, int, T], None]):
        for i in range(0, self.height):
            for j in range(0, self.width):
                item = self.get(i, j)
                if item is not None:
                    action(i, j, item)
