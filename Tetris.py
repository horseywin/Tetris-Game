from pynput import keyboard
import threading

import os
import time
import random
import math
import copy

def on_press(key):

    if  key == keyboard.Key.left:
            my_game.move_shape(current, -90)
    elif key == keyboard.Key.right:
        my_game.move_shape(current, 90)
    elif key == keyboard.Key.up:
        current.rotate_shape(next_rotation(current.rotation), my_game)

    # Exit when the 'Esc' key is pressed
    if key == keyboard.Key.esc:
        print("Exiting...")
        return False  # Stops the listener

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

listener_thread = threading.Thread(target=start_listener)
listener_thread.start()


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

    def main(self):
        global current
        my_game.apply_gravity()
        my_game.clear()
        my_game.update_shapes()
        os.system('clear')
        print(my_game.get_printable())
        time.sleep(1)


    def get_merged_rows(self):
        return list(map(lambda row: ''.join(row), self.contents))

    def get_printable(self):
        return '\n'.join(self.get_merged_rows())

    def insert_shape(self, shape, character):
        #print(f'INSERTING SHAPE: \n X = {shape.x} \n Y = {shape.y}')
        for x, y in shape.get_cords():
            if x >= 0:    
                try:
                    self.contents[y][x] = character
                except:
                    for x, y in shape.get_cords():
                        print('x', x)
                        print('y', y)
                    raise IndexError('failed to insert shape: index out of range')
                    
            #else:
                #print('REFUSED TO EXIT BORDER')

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
            print([y for x, y in shape.get_cords()])
            print([y < self.y - 1 for x, y in shape.get_cords()])
            if all([y < self.y - 1 for x, y in shape.get_cords()]):
                #print('gravity touch test', [self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords() for x, y in shape.get_cords()])
                if all([self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords() for x, y in shape.get_cords()]):   
                    #print("appling gravity")
                    shape.y += self.gravity_scale
            #else:
                #print('gravity stopped')
        
    def in_border(self, x, y):
        return all([x in range(0, self.x), y in range(0, self.y)])

    def is_valid(self, shape):
        #checks if the shape is valid
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
        #print('summoned shape')

    def move_shape(self, shape, direction, move_amount=1):
        #Makes an instance of the {shape} and checks if all the cords are valid
        if direction in [90, -90]:
            test = type(shape)(shape.x + (directions[direction] * move_amount), shape.y, shape.rotation, shape.color)
            if self.is_valid(type(test)(test.x, test.y, test.rotation, test.color)):
                if all([self.contents[y][x + directions[direction]] == colors['white'] or (x + directions[direction], y) in shape.get_cords() for x, y in shape.get_cords()]):
                    shape.x = test.x

            else:
                print('IS NOT VALID (test shape)')
    

class shape:
    def __init__(self, x, y, rotation, color):
        self.x = x
        self.y = y
        self.rotation = int(rotation)
        self.color = color

    def get_cords(self):
        print('UNDEFINED')

    def rotate_shape(self, direction, game):
        if direction in directions:
            print('SUCCESS: STARTING ROTATE FUNCTION')
            test = copy.deepcopy(self)
            test.rotation = direction
            if game.is_valid(test):
                print('VALID ROTATIONS: CHANGEING CORDS')
                self.rotation = direction
            else:
                print('NOT TECHNICALLY VALID...CANCELLING ROTATION')
        else:
            raise SyntaxError(f"{direction} does not exist")

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
        if self.rotation in [180, 0]:
            return [
            (self.x - 1, self.y),
            (self.x, self.y),
            (self.x + 1, self.y),
            (self.x + 2, self.y)
            ]
        elif self.rotation in [90, -90]:
            return [
            (self.x, self.y - 2),
            (self.x, self.y - 1),
            (self.x, self.y),
            (self.x, self.y + 1)
            ]

def next_rotation(current_direction):
    global directions
    if current_direction in directions:
        if current_direction == 90:
            return 180
        if current_direction == 180:
            return -90
        if current_direction == -90:
            return 0
        if current_direction == 0:
            return 90
    else:
        raise SyntaxError('DIRECTION NOT FOUND')

my_game = game()

my_game.add_shape(square(4, 10, 0, colors['yellow']))
current = my_game.summon_shape(line(3, 4, 90, colors['yellow']))
for i in range(5000):
    current = my_game.shapes[-1]
    my_game.main()

listener_thread.join()
#testing

"""
my_line = line(2, 3, 0)
my_game.insert_shape(my_line, '🟪')
print(my_line.get_cords())
print(my_game.get_printable())
"""
"""
for _ in range(100):
    my_line = line(random.randint(0, 8), random.randint(0, 15), 0)
    print(my_line.get_cords())
    my_game.insert_shape(my_line, '⬛')
    print(my_game.get_printable())
    time.sleep(0.1)
    my_game.clear()
    os.system('clear')
"""
"""
for y in range(10):
    my_game.clear()
    my_game.insert_shape(square(4, y, 0), '🟦')
    print(my_game.get_printable())
    time.sleep(0.1)
    os.system('clear')
"""