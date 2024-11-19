from pynput import keyboard
import threading
import os
import time
import random
import math
import copy

def on_press(key):
    global my_game
    global FORCE_STOP
    if  key == keyboard.Key.left:
            my_game.move_shape(current, -90)
    elif key == keyboard.Key.right:
        my_game.move_shape(current, 90)
    elif key == keyboard.Key.up:
        current.rotate_shape(next_rotation(current.rotation), my_game)
    elif key == keyboard.Key.down:
        my_game.apply_gravity([current])
        my_game.score += 1
        print('')

    # Exit when the 'Esc' key is pressed
    if key == keyboard.Key.esc:
        print("Exiting...")
        FORCE_STOP = True
        return False  # Stops the listener

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if str(input('DEBUG?')):
    debug = True
    frame_inspect = True
else:
    debug = False
    frame_inspect = False
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()
FORCE_STOP = False
summon_tick = None

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
    global all_shapes
    def __init__(self, x=10, y=20, gravity_scale=1, tick_speed=0.2):
        self.x = x
        self.y = y
        self.contents = [[colors['white'] for column in range(self.x)] for row in range(self.y)]
        self.shapes = []
        self.gravity_scale = gravity_scale
        self.tick_speed = tick_speed
        self.score = 0
    def main(self):
        global current
        global frame_inspect
        global summon_tick
        if not my_game.apply_gravity()[-1]:
            print('summon now')
            my_game.apply_gravity()
            if summon_tick == 3:
                self.summon_random_shape()
            else:
                summon_tick += 1
        else:
            summon_tick = 0
        my_game.apply_gravity()
        my_game.clear()
        my_game.update_shapes()
        if not frame_inspect:
            os.system('clear')
            print('\n')
        print(f'SCORE: {my_game.score}')
        print(my_game.get_printable())
        time.sleep(self.tick_speed)

    def get_merged_rows(self):
        return list(map(lambda row: ''.join(row), self.contents))

    def get_printable(self):
        return '\n'.join(self.get_merged_rows())
#tdjo ltuq yttj xxbn

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

    def apply_gravity(self, specifed_shape_list=[]):
        success_list = []
        if not specifed_shape_list:
            list_of_shapes = self.shapes
        else:
            list_of_shapes = specifed_shape_list
        for shape in list_of_shapes:
            if debug: print([y for x, y in shape.get_cords()])
            if debug: print([y < self.y - 1 for x, y in shape.get_cords()])
            if all([y < self.y - 1 for x, y in shape.get_cords()]):
                if debug: print('gravity touch test', [self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords() for x, y in shape.get_cords()])
                if all([self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords() for x, y in shape.get_cords()]):   
                    if debug: print("appling gravity")
                    shape.y += self.gravity_scale
                    success_list.append(True)
                else:
                    if debug: print('GRAVITY STOPPED DUE TO COLLISION OR OBSOLETE CORD')
                    success_list.append(False)
            else:
                if debug: print('gravity stopped')
                success_list.append(False)
        return success_list
    def in_border(self, x, y):
        return all([x in range(0, self.x), y in range(0, self.y)])

    def is_valid(self, shape):
        #checks if the shape is valid
        return all([self.in_border(x, y) for x, y in shape.get_cords()])

    
    def summon_specifed_shape(self, shape):
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
                    return True
                else:
                    if debug: print('ANOTHER SHAPE IS IN THE WAY: SHAPE TYPE', type(shape))
                    return False
            else:
                if debug: print('IS NOT VALID (test shape)')
                return False
        else:
            return False

    def is_shape_movable(self, shape):

        test_left = type(shape)(shape.x - 1, shape.y, shape.rotation, shape.color)
        can_move_left = self.is_valid(test_left) and all(
            [self.contents[y][x - 1] == colors['white'] or (x - 1, y) in shape.get_cords() for x, y in shape.get_cords()]
        )

        test_right = type(shape)(shape.x + 1, shape.y, shape.rotation, shape.color)
        can_move_right = self.is_valid(test_right) and all(
            [self.contents[y][x + 1] == colors['white'] or (x + 1, y) in shape.get_cords() for x, y in shape.get_cords()]
        )
        return can_move_left or can_move_right

    def summon_random_shape(self):
        random_color = colors['white']
        while random_color == colors['white']:
            random_color = random.choice(list(colors.values()))
        return self.add_shape(type(random.choice(all_shapes))(
        self.x // 2 - 1,
        0,
        random.choice(rotations),
        random_color)
        )


class shape:
    def __init__(self, x, y, rotation, color):
        self.x = x
        self.y = y
        self.rotation = int(rotation)
        self.color = color

    def get_cords(self):
        if debug: print('UNDEFINED')

    def rotate_shape(self, direction, game):
        if direction in directions:
            if debug: print('SUCCESS: STARTING ROTATE FUNCTION')
            test = copy.deepcopy(self)
            test.rotation = direction
            if game.is_valid(test):
                if debug: print('VALID ROTATIONS: CHANGEING CORDS')
                self.rotation = direction
            else:
                if debug: print('NOT TECHNICALLY VALID...CANCELLING ROTATION')
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

#defining all shapes with examples:

all_shapes = [
    square(1, 2, 90, colors['red']), 
    line(1, 1, 90, colors['black'])
]

my_game = game()

my_game.add_shape(square(4, 10, 0, colors['yellow']))

while True:
    if not FORCE_STOP:
        current = my_game.shapes[-1]
        my_game.main()
    else:
        if debug: print("STOPPING ALL PROCESSES")

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