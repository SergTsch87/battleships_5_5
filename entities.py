# Entities:
    # Field
    # Ship
    # Gamer
    # Shot

class Field:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols


class Ship:
    def __init__(self, cells, state):
        self.cells = cells # cells == [[x, y], [x, y], ...] OR cells == {(x,y), (x,y), ...}
        self.state = state # whole / damaged / destroyed


class Gamer:
    def __init__(self):
        # список кораблів певного гравця
        # стан поточного та наступного ходу: 0 / 1
        pass


class Shot:
    def __init__(self, cell, state):
        self.cell = cell
        self.state = state # Чи це тут треба?..