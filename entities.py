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
    """
    Клас Field представляє ігрове поле для гри "Морський бій".
    Керує розміщенням кораблів, обробкою пострілів та станом клітин поля.
    """
    
    # Константи для стану клітин
    EMPTY = 0      # Клітина порожня
    SHIP = 1       # На клітині знаходиться корабель
    HIT = 2        # Постріл влучив у корабель
    MISS = 3       # Постріл промахнувся
    
    def __init__(self, rows, cols):
        """
        Ініціалізує поле з вказаними розмірами.
        
        Args:
            rows (int): Кількість рядків поля
            cols (int): Кількість стовпців поля
        """
        self.rows = rows
        self.cols = cols
        # Двовимірна сітка для зберігання стану кожної клітини
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
        # Словник для швидкого доступу до кораблів за координатами
        self.ships_map = {}  # {(x, y): Ship}
        # Список усіх кораблів на полі
        self.ships = []
        # Множина координат пострілів для швидкої перевірки
        self.shots = set()  # {(x, y), ...}
    
    def is_valid_coordinate(self, x, y):
        """
        Перевіряє, чи координата в межах поля.
        
        Args:
            x (int): Координата X (рядок)
            y (int): Координата Y (стовпець)
            
        Returns:
            bool: True, якщо координата в межах, False інакше
        """
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def get_cell(self, x, y):
        """
        Повертає стан клітини.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            
        Returns:
            int: Стан клітини (EMPTY, SHIP, HIT, MISS)
        """
        if not self.is_valid_coordinate(x, y):
            return None
        return self.grid[x][y]
    
    def set_cell(self, x, y, state):
        """
        Встановлює стан клітини.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            state (int): Новий стан клітини
            
        Returns:
            bool: True, якщо операція успішна, False інакше
        """
        if not self.is_valid_coordinate(x, y):
            return False
        self.grid[x][y] = state
        return True
    
    def get_adjacent_cells(self, x, y):
        """
        Повертає список суміжних клітин (включаючи діагоналі).
        Використовується для перевірки, щоб кораблі не торкалися.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            
        Returns:
            list: Список кортежів (x, y) суміжних клітин
        """
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_coordinate(nx, ny):
                    adjacent.append((nx, ny))
        return adjacent
    
    def can_place_ship(self, ship):
        """
        Перевіряє, чи можна розмістити корабель на полі.
        Перевіряє:
        - Усі клітини в межах поля
        - Клітини порожні (не занято іншими кораблями)
        - Корабель не торкається інших кораблів (включаючи діагоналі)
        
        Args:
            ship (Ship): Об'єкт корабля для розміщення
            
        Returns:
            bool: True, якщо корабель можна розмістити, False інакше
        """
        # Перевірка, чи всі клітини корабля в межах поля
        for x, y in ship.cells:
            if not self.is_valid_coordinate(x, y):
                return False
        
        # Перевірка, чи клітини корабля порожні
        for x, y in ship.cells:
            if self.grid[x][y] != self.EMPTY:
                return False
        
        # Перевірка, чи корабель не торкається інших кораблів
        for x, y in ship.cells:
            for adj_x, adj_y in self.get_adjacent_cells(x, y):
                if self.grid[adj_x][adj_y] == self.SHIP:
                    return False
        
        return True
    
    def place_ship(self, ship):
        """
        Розміщує корабель на полі.
        
        Args:
            ship (Ship): Об'єкт корабля для розміщення
            
        Returns:
            bool: True, якщо корабель успішно розміщений, False інакше
        """
        if not self.can_place_ship(ship):
            return False
        
        # Розміщуємо корабель на сітці
        for x, y in ship.cells:
            self.grid[x][y] = self.SHIP
            self.ships_map[(x, y)] = ship
        
        # Додаємо корабель до списку
        self.ships.append(ship)
        return True
    
    def process_shot(self, x, y):
        """
        Обробляє постріл за координатами.
        
        Args:
            x (int): Координата X
            y (int): Координата Y
            
        Returns:
            dict: {'hit': bool, 'ship_destroyed': bool, 'already_shot': bool}
                - hit: True, якщо постріл влучив у корабель
                - ship_destroyed: True, якщо корабель знищений
                - already_shot: True, якщо в цю клітину вже стріляли
        """
        if not self.is_valid_coordinate(x, y):
            return {'hit': False, 'ship_destroyed': False, 'already_shot': True}
        
        # Перевірка, чи вже було пострілу в цю клітину
        if (x, y) in self.shots:
            return {'hit': False, 'ship_destroyed': False, 'already_shot': True}
        
        self.shots.add((x, y))
        cell_state = self.grid[x][y]
        
        # Випадок 1: Постріл у порожню клітину (промах)
        if cell_state == self.EMPTY:
            self.grid[x][y] = self.MISS
            return {'hit': False, 'ship_destroyed': False, 'already_shot': False}
        
        # Випадок 2: Постріл у корабель (влучення)
        elif cell_state == self.SHIP:
            self.grid[x][y] = self.HIT
            ship = self.ships_map.get((x, y))
            
            if ship is None:
                return {'hit': True, 'ship_destroyed': False, 'already_shot': False}
            
            # Оновлюємо стан корабля
            ship.take_hit(x, y)
            
            # Перевіряємо, чи корабель знищений
            is_destroyed = ship.is_destroyed()
            
            return {'hit': True, 'ship_destroyed': is_destroyed, 'already_shot': False}
        
        # Випадок 3: Повторний постріл у вже влучену або промахнуту клітину
        else:
            return {'hit': False, 'ship_destroyed': False, 'already_shot': True}
    
    def is_all_ships_destroyed(self):
        """
        Перевіряє, чи всі кораблі на полі знищені.
        
        Returns:
            bool: True, якщо всі кораблі знищені, False інакше
        """
        return all(ship.is_destroyed() for ship in self.ships)
    
    def __str__(self):
        """
        Повертає рядкове представлення поля для відображення.
        
        Returns:
            str: Візуальне представлення поля
        """
        symbols = {
            self.EMPTY: '~',
            self.SHIP: '🚢',
            self.HIT: '💥',
            self.MISS: '•'
        }
        
        lines = []
        for row in self.grid:
            lines.append(' '.join(symbols.get(cell, '?') for cell in row))
        
        return '\n'.join(lines)


class Ship:
    """
    Клас Ship представляє корабель для гри "Морський бій".
    Керує станом корабля, його клітинами та перевіркою знищення.
    """
    
    # Константи для стану корабля
    WHOLE = 0      # Корабель неушкоджений
    DAMAGED = 1    # Корабель ушкоджений, але не знищений
    DESTROYED = 2  # Корабель повністю знищений
    
    def __init__(self, cells, length=None):
        """
        Ініціалізує корабель.
        
        Args:
            cells (list, tuple, set): Набір координат клітин корабля [(x, y), ...]
            length (int, optional): Довжина корабля (автоматично визначається за кількістю клітин)
        """
        # Конвертуємо cells у множину для швидкого пошуку
        if isinstance(cells, (list, tuple)):
            self.cells = set(cells)
        else:
            self.cells = cells  # Припускаємо, що це вже множина
        
        # Довжина корабля
        self.length = length if length else len(self.cells)
        
        # Стан корабля
        self.state = self.WHOLE
        
        # Множина влучених клітин
        self.hit_cells = set()
    
    def take_hit(self, x, y):
        """
        Фіксує влучення у клітину корабля.
        Оновлює стан корабля на основі кількості влучень.
        
        Args:
            x (int): Координата X влучення
            y (int): Координата Y влучення
            
        Returns:
            bool: True, якщо влучення успішне, False якщо цю клітину вже було влучено
        """
        if (x, y) not in self.cells:
            return False
        
        if (x, y) in self.hit_cells:
            return False  # Це клітину вже було влучено
        
        self.hit_cells.add((x, y))
        
        # Оновлюємо стан корабля
        if len(self.hit_cells) == self.length:
            self.state = self.DESTROYED
        elif len(self.hit_cells) > 0:
            self.state = self.DAMAGED
        
        return True
    
    def is_damaged(self):
        """
        Перевіряє, чи корабель пошкоджений.
        
        Returns:
            bool: True, якщо корабель має влучення, False інакше
        """
        return len(self.hit_cells) > 0 and len(self.hit_cells) < self.length
    
    def is_destroyed(self):
        """
        Перевіряє, чи корабель знищений.
        
        Returns:
            bool: True, якщо корабель повністю знищений, False інакше
        """
        return self.state == self.DESTROYED or len(self.hit_cells) == self.length
    
    def get_health(self):
        """
        Повертає кількість неушкоджених клітин корабля.
        
        Returns:
            int: Кількість клітин, які ще не були влучені
        """
        return self.length - len(self.hit_cells)
    
    def __str__(self):
        """
        Повертає рядкове представлення корабля.
        
        Returns:
            str: Інформація про корабель
        """
        states = {self.WHOLE: "Неушкоджений", self.DAMAGED: "Ушкоджений", self.DESTROYED: "Знищений"}
        return f"Корабель (довжина {self.length}): {states[self.state]} - {self.get_health()} клітин залишилось"


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