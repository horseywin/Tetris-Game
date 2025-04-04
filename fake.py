
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


    # Exit when the 'Esc' key is pressed
    if key == keyboard.Key.esc:
        print("Exiting...")
        FORCE_STOP = True
        return False  # Stops the listener

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def game_over_text():
    # Text art for "Game Over"
    game_over_text = """    
    ░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
    ██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
    ██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
    ██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
    ╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
    ░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
    """
    
    # Clear the screen
    os.system("clear")
    
    # Animation loop to simulate the "Game Over" text appearing with a slight delay
    for line in game_over_text.splitlines():
        print(line)
        time.sleep(0.5)  # Delay between each line of the text art
    

if False:
    debug = True
    frame_inspect = True
else:
    debug = False
    frame_inspect = False


listener_thread = threading.Thread(target=start_listener)
listener_thread.start()
FORCE_STOP = False
summon_tick = None

game_over = False
number_art = {
    '0': [
        "░█████╗░",
        "██╔══██╗",
        "██║░░██║",
        "██║░░██║",
        "╚█████╔╝",
        "░╚════╝░"
    ],
    '1': [     
        "░░███╗░░",
        "░████║░░",
        "██╔██║░░",
        "╚═╝██║░░",
        "███████╗",
        "╚══════╝"
    ],
    '2': [
        "██████╗░",
        "╚════██╗",
        "░░███╔═╝",
        "██╔══╝░░",
        "███████╗",
        "╚══════╝"
    ],
    '3': [
        "██████╗░",
        "╚════██╗",
        "░█████╔╝",
        "░╚═══██╗",
        "██████╔╝",
        "╚═════╝░"
    ],
    '4': [
        "░░██╗██╗",
        "░██╔╝██║",
        "██╔╝░██║",
        "███████║",
        "╚════██║",
        "░░░░░╚═╝"
    ],
    '5': [
        "███████╗",
        "██╔════╝",
        "██████╗░",
        "╚════██╗",
        "██████╔╝",
        "╚═════╝░"
    ],
    '6': [
        "░█████╗░",
        "██╔═══╝░",
        "██████╗░",
        "██╔══██╗",
        "╚█████╔╝",
        "░╚════╝░"
    ],
    '7': [
        "███████╗",
        "╚════██║",
        "░░░░██╔╝",
        "░░░██╔╝░",
        "░░██╔╝░░",
        "░░╚═╝░░░"
    ],
    '8': [
        "░█████╗░",
        "██╔══██╗",
        "╚█████╔╝",
        "██╔══██╗",
        "╚█████╔╝",
        "░╚════╝░"
    ],
    '9': [
        "░█████╗░"
        "██╔══██╗",
        "╚██████║",
        "░╚═══██║",
        "░█████╔╝",
        "░╚════╝░"
    ]
}


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
    def __init__(self, x=10, y=20, gravity_scale=1, tick_speed=0.4):
        self.x = x
        self.y = y
        self.contents = [[colors['white'] for column in range(self.x)] for row in range(self.y)]
        self.shapes = []
        self.gravity_scale = gravity_scale
        self.tick_speed = tick_speed
        self.score = 0
        self.level = 1
        self.current_rows_cleared = 0
    
    def main(self):
        global current
        global frame_inspect
        global summon_tick
        #if not success list?!!
        if not copy.deepcopy(my_game).apply_gravity()[-1]:
            my_game.apply_gravity()
            if summon_tick == 3:
                my_game.scan_for_combos()
                random_shape = self.summon_random_shape()
            else:
                summon_tick += 1
        else:
            summon_tick = 0
        my_game.apply_gravity()
       
        time.sleep(self.tick_speed)

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

    def apply_gravity(self, specifed_shape_list=[]):
        global game_over
        success_list = []
        if not specifed_shape_list:
            list_of_shapes = self.shapes
        else:
            list_of_shapes = specifed_shape_list
        for shape in list_of_shapes:
            if all([y < self.y - 1 for x, y in shape.get_cords()]):
                if all([(y+1 < self.y and (self.contents[y+1][x] == colors['white'] or (x, y+1) in shape.get_cords())) for x, y in shape.get_cords()]):   
                    if debug: print("appling gravity")
                    shape.y += self.gravity_scale
                    #Refresh
                    os.system('clear')
                    print(f'SCORE: {my_game.score}    LEVEL: {my_game.level}')
                    print(my_game.get_printable())
                    my_game.clear()
                    my_game.update_shapes()
                    #end of refresh script
                    success_list.append(True)
                else:
                    if debug: print('GRAVITY STOPPED DUE TO COLLISION OR OBSOLETE CORD')
                    if all([y == 0 
                    for x, y in shape.get_cords()]):
                        game_over = True
                        print("I SAID GAME OVER!!!")

                    success_list.append(True)
            else:
                if debug: print('gravity stopped')
                success_list.append(False)
        return success_list
    def in_border(self, x, y):
        return all([x in range(0, self.x), y in range(0, self.y)])

    def is_valid(self, test_shape, original_shape):
        #checks if the shape is valid
        test_contents = copy.deepcopy(self.contents)
        #Remove original shape from copy test cords
        for x, y in original_shape.get_cords():
            test_contents[y][x] = colors['white']
        
        return all([self.in_border(x, y) and test_contents[y][x] == colors['white'] for x, y in test_shape.get_cords()])

    
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
            if self.is_valid(type(test)(test.x, test.y, test.rotation, test.color), shape):
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
    """
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
    """
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

    """
    •	Single (1 line cleared): 100 points x current level.
	•	Double (2 lines cleared): 300 points x current level.
	•	Triple (3 lines cleared): 500 points x current level.
	•	Tetris (4 lines cleared at once): 800 points x current level.
    """

    def scan_for_combos(self):
        line_combos = 0
        for index, row in enumerate(self.contents):
            #Check if all sqaures in a line is white
            if all([sqaure != colors['white'] for sqaure in row]):
                line_combos += 1
                #scan though shapes
                for shape in self.shapes:
                    #scan though cords in each shape
                    for cord in shape.get_cords():
                        #Checking if the indevidual sqaure matches one of the sqaures in the selected row
                        if cord in [(x, index) for x in range(0, self.x + 1)]:
                            #90: [(0, 0),(1, 0),(1, 1),(0, 1)]
                            #for each cord in blueprint
                            for x, y in shape.blueprint[shape.rotation]:
                                if cord == (shape.x + x, shape.y + y):
                                    shape.blueprint[shape.rotation].pop(shape.blueprint[shape.rotation].index((x, y)))
                                    os.system('clear')
                                    print(f'SCORE: {my_game.score}    LEVEL: {my_game.level}')
                                    print(my_game.get_printable())
                                    my_game.clear()
                                    my_game.update_shapes()
                                    time.sleep(0.05)
                            self.current_rows_cleared += 0.10
        
                                        
                            
        if line_combos == 1:
            self.score += 100 * self.level
        elif line_combos == 2:
            self.score += 300 * self.level
        elif line_combos == 3:
            self.score += 500 * self.level
        elif line_combos == 4:
            self.score += 800 * self.level
        

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
            if game.is_valid(test, self):
                if debug: print('VALID ROTATIONS: CHANGEING CORDS')
                self.rotation = direction
            else:
                if debug: print('NOT TECHNICALLY VALID...CANCELLING ROTATION')
        else:
            raise SyntaxError(f"{direction} does not exist")
    
    def get_cords(self):
        return [(self.x + x, self.y + y) for x, y in self.blueprint[self.rotation]]

class up_left(shape):
    def __init__(self, x, y, rotation, color):
        super().__init__(x, y, rotation, color)
        self.blueprint = {
            #working
            90: [
            (0, 0),
            (1, 0),
            (2, 0),
            (0, 1)
            ],
            #working
            180: [
            (0, 0),
            (1, 0),
            (1, 1),
            (1, 2)
            ],
            -90: [
            (0, 1),
            (1, 1),
            (2, 1),
            (2, 0)
            ],
            
            0: [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
            ],
        }

class square(shape):

    def __init__(self, x, y, rotation, color):
        super().__init__(x, y, rotation, color)
        self.blueprint = {
            0: [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
            ],
            90: [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
            ],
            -90: [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
            ],
            180: [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
            ],
        }
        
class line(shape):
    def __init__(self, x, y, rotation, color):
        super().__init__(x, y, rotation, color)
        self.blueprint = {
            90: [
            (0, -2),
            (0, -1),
            (0, 0),
            (0, 1)
            ],
            -90: [
            (0, -2),
            (0, -1),
            (0, 0),
            (0, 1)
            ],
            180: [
            (-1, 0),
            (0, 0),
            (1, 0),
            (2, 0)
            ],
            0: [
            (-1, 0),
            (0, 0),
            (1, 0),
            (2, 0)
            ],
        }

class t_arch(shape):
    def __init__(self, x, y, rotation, color):
        super().__init__(x, y, rotation, color)
        self.blueprint = {
            180: [
            (0, 0),
            (1, 0),
            (2, 0),
            (1, 1)
            ],
            -90: [
            (1, 0),
            (1, 1),
            (0, 1),
            (1, 2)
            ],
            90: [
            (0, 0),#
            (0, 1),#
            (1, 1),#
            (0, 2)
            ],
            0: [
            (1, 0),
            (0, 1),
            (1, 1),
            (2, 1)
            ],
        }

class up_right(shape):
    def __init__(self, x, y, rotation, color):
        super().__init__(x, y, rotation, color)
        self.blueprint = {
            #working
            -90: [
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1)
            ],
            #working
            180: [
            (0, 0),
            (1, 0),
            (0, 1),
            (0, 2)
            ],
            90: [
            (0, 0),
            (0, 1),
            (1, 1),
            (2, 1)
            ],
            
            0: [
            (1, 0),
            (1, 1),
            (1, 2),
            (0, 2)
            ],
        }

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
    line(1, 1, 90, colors['black']),
    up_left(1, 1, 90, colors['black']),
    t_arch(1, 1, 90, colors['black']),
    up_right(1, 1, 90, colors['black'])
]

def update_frame():
    global my_game
    global FORCE_STOP
    global game_over
    while True:
        if not game_over and not FORCE_STOP:
            
            os.system('clear')
            print(f'SCORE: {my_game.score}    LEVEL: {my_game.level}')
            print(my_game.get_printable())
            my_game.clear()
            my_game.update_shapes()
            time.sleep(0.05)

my_game = game()


my_game.summon_random_shape()
#my_game.summon_specifed_shape(up_right(1, 1, 90, colors['black']),)
level_score = 0
#main game loop (this makes the game run!)

def init_game_over():
    global my_game
    global FORCE_STOP
    time.sleep(0.5)
    print('    ' + 75 * '_')
    print(
        f"""
    ░██████╗░█████╗░░█████╗░██████╗░███████╗
    ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ╚█████╗░██║░░╚═╝██║░░██║██████╔╝█████╗░░
    ░╚═══██╗██║░░██╗██║░░██║██╔══██╗██╔══╝░░
    ██████╔╝╚█████╔╝╚█████╔╝██║░░██║███████╗
    ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝
"""
    )
    number_result = ""
    for layer in range(6):
        layer_result = ""
        for number in str(my_game.score):
            try:
                layer_result += str(number_art[number][layer])
            except:
                print("ERROR")
        number_result += '    ' + layer_result + '\n'
    print(number_result)
    if str(input(f"""
    {75 * '_'}

    ██████╗░██╗░░░░░░█████╗░██╗░░░██╗  ░█████╗░░██████╗░░█████╗░██╗███╗░░██╗░█████╗░
    ██╔══██╗██║░░░░░██╔══██╗╚██╗░██╔╝  ██╔══██╗██╔════╝░██╔══██╗██║████╗░██║██╔══██╗
    ██████╔╝██║░░░░░███████║░╚████╔╝░  ███████║██║░░██╗░███████║██║██╔██╗██║╚═╝███╔╝
    ██╔═══╝░██║░░░░░██╔══██║░░╚██╔╝░░  ██╔══██║██║░░╚██╗██╔══██║██║██║╚████║░░░╚══╝░
    ██║░░░░░███████╗██║░░██║░░░██║░░░  ██║░░██║╚██████╔╝██║░░██║██║██║░╚███║░░░██╗░░
    ╚═╝░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚══╝░░░╚═╝░░

    ██╗░░░██╗░░░░██╗███╗░░██╗
    ╚██╗░██╔╝░░░██╔╝████╗░██║
    ░╚████╔╝░░░██╔╝░██╔██╗██║
    ░░╚██╔╝░░░██╔╝░░██║╚████║
    ░░░██║░░░██╔╝░░░██║░╚███║
    ░░░╚═╝░░░╚═╝░░░░╚═╝░░╚══╝
""")) == 'y':
        print('resetting game...')
        game_over = False
        FORCE_STOP = False


os.system("clear")
print("""

████████╗███████╗████████╗██████╗░██╗░██████╗
╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝
░░░██║░░░█████╗░░░░░██║░░░██████╔╝██║╚█████╗░
░░░██║░░░██╔══╝░░░░░██║░░░██╔══██╗██║░╚═══██╗
░░░██║░░░███████╗░░░██║░░░██║░░██║██║██████╔╝
░░░╚═╝░░░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═════╝░
"""
)

if input("""
    
    

█▀█ █▀█ █▀▀ █▀ █▀   █▀▀ █▄░█ ▀█▀ █▀▀ █▀█   ▀█▀ █▀█   █▀ ▀█▀ ▄▀█ █▀█ ▀█▀
█▀▀ █▀▄ ██▄ ▄█ ▄█   ██▄ █░▀█ ░█░ ██▄ █▀▄   ░█░ █▄█   ▄█ ░█░ █▀█ █▀▄ ░█░

"""): pass
frame_thead = threading.Thread(target=update_frame, daemon=True)
frame_thead.start()
while True:
    if not FORCE_STOP and not game_over:
        current = my_game.shapes[-1]
        my_game.main()
        #speed things up based on time
        
        if my_game.current_rows_cleared >= my_game.level * 10:
            my_game.current_rows_cleared = 0
            my_game.level += 1
            if my_game.tick_speed > 0.01:
                my_game.tick_speed -= 0.05
    elif game_over:
        game_over_text()
        init_game_over()
        game_over = False
        my_game = copy.deepcopy(game())
        my_game.summon_random_shape()
        continue
    else:
        break

listener_thread.join()
#testing
