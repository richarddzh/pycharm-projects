def last_index(a_list, func):
    for i in range(len(a_list) - 1, -1, -1):
        if func(a_list[i]):
            return i
    return -1


class Array2D:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.rows = []

    def set(self, y, x, elem):
        if y >= self.height:
            self.height = y + 1
        if x >= self.width:
            self.width = x + 1
        while len(self.rows) < self.height:
            self.rows.append([])
        while len(self.rows[y]) < self.width:
            self.rows[y].append(None)
        self.rows[y][x] = elem

    def get(self, y, x):
        if y >= len(self.rows):
            return None
        if x >= len(self.rows[y]):
            return None
        return self.rows[y][x]
