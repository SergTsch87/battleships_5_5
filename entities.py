# Entities:
    # Game
    # Field
    # Ship
    # Gamer

# Стан гри:
#   Додайте центральний клас Game, який керує двома гравцями,
#   чергою ходів і перевіркою перемоги. Це відокремить логіку
#   від класів сутностей.

class Game:
    def __init__(self, Gamer):
        pass


class Field:
    def __init__(self, rows, cols, state_cells):
        self.rows = rows
        self.cols = cols
        self.state_cells = state_cells # state_cells == {x:.., y:.., state: emp | fill | влучена | промах}
    
    # клас повинен зберігати стан поля
    #   (де розташовані кораблі, де були постріли)

    def border_check(self, x, y):
        if 0 < x <= self.x:
            return True
        else:
            return False
        
    def checking_for_ships_collisions():
        pass

    def chot_processing():
        pass


class Ship:
    def __init__(self, cells, state):
        self.cells = cells # cells == [[x, y], [x, y], ...] OR cells == {(x,y), (x,y), ...}
        self.state = state # whole / damaged / destroyed


class Gamer:
    def __init__(self, name, state_step):
        self.name = name
        self.state_step = state_step # булевий прапорець (is_turn) або лічильник, щоб керувати чергою

        # список кораблів (як екземпляри Ship)
        # власне поле (екземпляр Field)
        # можливо, список пострілів / історію ходів
        
        # список кораблів певного гравця
        # стан поточного та наступного ходу: 0 / 1
        

# class Shot:
#     def __init__(self, cell, state):
#         self.cell = cell
#         self.state = state # Чи це тут треба?..