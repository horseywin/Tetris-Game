import curses
import time
import random
import math
from curses import wrapper

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.clear() 
    colors = {
        'red':'🟥',
        'orange':'🟧',
        'yellow':'🟨',
        'green': '🟩',
        'blue': '🟦',
        'pink': '🟪',
        'brown': '🟫',
        'black': '⬛',
        'white': '⬜'
        }

    rotations = [
        0,
        90,
        180,
        -90
    ]

    directions = {
        90: 1,
        0: 1,
        -90: -1,
        180: -1,
        
    }

    class game:
        def __init__(self, x=10, y=20, gravity_scale=1):
            self.x = x
            self.y = y
            self.contents = [[colors['white'] for column in range(self.x)] for row in range(self.y)]
            self.shapes = []
            self.gravity_scale = gravity_scale

        def get_merged_rows(self):
            return list(map(lambda row: ''.join(row), self.contents))

        def get_printable(self):
            return '\n'.join(self.get_merged_rows())

        def insert_shape(self, shape, character):
            stdscr.addstr(f'INSERTING SHAPE: \n X = {shape.x} \n Y = {shape.y}')
            for x, y in shape.get_cords():
                if x >= 0:    
                    try:
                        self.contents[y][x] = character
                    except:
                        raise IndexError('failed to insert shape: index out of range')

        def clear(self):
            self.contents = [[colors['white'] for column in range(self.x)] for row in range(self.y)]

        def add_shape(self, shape):
            self.shapes.append(shape)
            return shape

        def update_shapes(self):
            for shape in self.shapes:  
                    self.insert_shape(shape, shape.color)

        def apply_gravity(self):
            
            for shape in self.shapes:
                if all([y < self.y - 1 for x, y in shape.get_cords()]):
                    if all([self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords() for x, y in shape.get_cords()]):   
                        shape.y += self.gravity_scale
            
        def in_border(self, x, y):
            return all([x in range(0, self.x), y in range(0, self.y)])

        def is_valid(self, shape):
            return all([self.in_border(x, y) for x, y in shape.get_cords()])

        
        def summon_shape(self, shape):
            random_color = colors['white']
            while random_color == colors['white']:
                random_color = random.choice(list(colors.values()))
            return self.add_shape(type(shape)(
            self.x // 2 - 1,
            0,
            random.choice(rotations),
            random_color)
            )

        def move_shape(self, shape, direction, move_amount=1):
            #Makes an instance of the {shape} and checks if all the cords are valid
            if direction in [90, -90]:
                test = type(shape)(shape.x + (directions[direction] * move_amount), shape.y, shape.rotation, shape.color)
                if self.is_valid(type(test)(test.x, test.y, test.rotation, test.color)):
                    shape.x = test.x

    class shape:
        def __init__(self, x, y, rotation, color):
            self.x = x
            self.y = y
            self.rotation = int(rotation)
            self.color = color

    class square(shape):
        def get_cords(self):
            return [
                (self.x, self.y),
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x, self.y + 1)
                ]

    class line(shape):
        def get_cords(self):
            if self.rotation == 90 or self.rotation == -90:
                return [
                (self.x, self.y),
                (self.x + 1, self.y),
                (self.x + 2, self.y),
                (self.x + 3, self.y)
                ]
            else:
                return [
                (self.x, self.y),
                (self.x, self.y + 1),
                (self.x, self.y + 2),
                (self.x, self.y + 3)
                ]

    my_game = game()
    my_game.add_shape(square(4, 10, 0, colors['yellow']))
    current = my_game.summon_shape(line(3, 4, 90, colors['yellow']))
    while True:
        stdscr.addstr('yeet')
        current = my_game.shapes[-1]
        key = stdscr.getch()
        my_game.apply_gravity()
        my_game.move_shape(current, -90)
        my_game.clear()
        my_game.update_shapes()
        stdscr.clear()
        stdscr.addstr(my_game.get_printable())
        time.sleep(0.2)
        if key == ord('q'):  # Press 'q' to quit
            break


wrapper(main)