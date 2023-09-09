import keyboard
import os
import time
import math
from PIL import Image
from window import Runtime

class Robject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 3
        self.h = 3
        self.screen= None
    def update(self,x_pos,y_pos):

        rectangle = self.draw_object()

        for y in range(len(rectangle)):
            for x in range(len(rectangle[0])):
                self.screen[y_pos + y][x_pos + x] = rectangle[y][x]

        return  self.screen


    def draw_object(self):
        matrix = [[""],[""],[""]]

        return matrix


class Renderer:
    def __init__(self,width,height,background = "`"):
        background = " " if background == "" else background
        self.background = background
        self.width = width
        self.height = height
        screen = []
        y_screen = []
        for i in range(self.height):
            for i in range(self.width):

                y_screen.append(self.background)
            screen.append(y_screen)
            y_screen = []

        self.screen = screen


    def refresh(self):

        screen = []
        y_screen = []
        for i in range(self.height):
            for i in range(self.width):

                y_screen.append(self.background)
            screen.append(y_screen)
            y_screen = []
        self.screen = screen


    def draw_screen(self):
        renderer = []
        for s in self.screen:
            f = "".join(s)
            renderer.append(f)
        return "\n".join(renderer)








class Cube(Robject):
    def __init__(self,renderer : Renderer,width,height,x = 0,y = 0,filled = False,transparent = False,):
        super(Cube,self).__init__()
        self.id = id
        self.w = width
        self.h = height
        self.filled = filled
        self.transparent = transparent
        if filled and transparent:
            raise AttributeError("an object cannot be filled but also transparent")
        self.x = x
        self.y = y
        self.renderer = renderer


    def update(self,x_pos,y_pos):
        screen = self.renderer.screen
        self.x = x_pos
        self.y = y_pos




        rectangle = self.draw_object()
        
        if self.filled:
            for y in range(len(rectangle)):
                for x in range(len(rectangle[0])):
                    try:
                        screen[y_pos + y][x_pos + x] = rectangle[y][x].replace(str(self.id), "|")
                    except IndexError:
                        screen[0][0] = self.renderer.background
        elif self.transparent:
            for y in range(len(rectangle)):
                for x in range(len(rectangle[0])):
                    try:
                        screen[y_pos + y][x_pos + x] = rectangle[y][x].replace(str(self.id), self.renderer.background)
                    except IndexError:
                        screen[0][0] = self.renderer.background
        else:       
            for y in range(len(rectangle)):
                for x in range(len(rectangle[0])):
                    try:
                        screen[y_pos + y][x_pos + x] = rectangle[y][x].replace(str(self.id), " ")
                    except IndexError:
                        screen[0][0] = self.renderer.background
        
        self.renderer.screen = screen



    def draw_object(self):
        matrix = [[str(self.id) for _ in range(self.w)] for _ in range(self.h)]

        # Draw the top edge
        matrix[0] = ['+' if i == 0 or i == self.w - 1 else '-' for i in range(self.w)]

        # Draw the sides
        for i in range(1, self.h - 1):
            matrix[i][0] = '|'
            matrix[i][self.w - 1] = '|'

        # Draw the bottom edge
        matrix[self.h - 1] = ['+' if i == 0 or i == self.w - 1 else '-' for i in range(self.w)]

        return matrix




class Circle(Robject):
    def __init__(self,renderer: Renderer, width, height):
        super(Circle, self).__init__()
        self.w = width
        self.h = height
        self.x = None
        self.y = None
        self.renderer = renderer
    def update(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        screen = self.renderer.screen
        circle = self.draw_object()

        for y in range(len(circle)):
            for x in range(len(circle[y])):
                if circle[y][x] == '*':
                    screen[y_pos + y][x_pos + x] = circle[y][x]
        self.renderer.screen = screen

    def draw_object(self):
        circle = [[' ' for _ in range(self.w)] for _ in range(self.h)]

        radius_x = self.w // 2
        radius_y = self.h // 2
        center_x = radius_x
        center_y = radius_y

        for y in range(self.h):
            for x in range(self.w):
                if math.pow((x - center_x) / radius_x, 2) + math.pow((y - center_y) / radius_y, 2) <= 1:
                    circle[y][x] = '*'

        return circle


class Triangle(Robject):
    def __init__(self,renderer: Renderer, width, height):
        super(Triangle, self).__init__()
        self.w = width
        self.h = height
        self.x = None
        self.y = None
        self.renderer = renderer
    def update(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        screen = self.renderer.screen
        triangle = self.draw_object()

        for y in range(len(triangle)):
            for x in range(len(triangle[y])):
                if triangle[y][x] != ' ':
                    screen[y_pos + y][x_pos + x] = triangle[y][x]
        self.renderer.screen = screen

    def draw_object(self):
        triangle = [[' ' for _ in range(self.w)] for _ in range(self.h)]

        for y in range(self.h):
            for x in range((self.w - y) // 2, (self.w + y) // 2 + 1):
                triangle[y][x] = '*'

        return triangle


class Custom(Robject):
    def __init__(self,renderer: Renderer, image_path, width, height):
        super(Custom, self).__init__()

        self.image_path = image_path
        self.w = width
        self.h = height
        self.x = None
        self.y = None
        self.renderer = renderer
    def update(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        screen = self.renderer.screen
        custom_shape = self.draw_object()

        for y in range(len(custom_shape)):
            for x in range(len(custom_shape[y])):
                screen[y_pos + y][x_pos + x] = custom_shape[y][x].replace(f"<bg>", self.renderer.background)
        self.renderer.screen = screen

    def draw_object(self):
        custom_shape = [[' ' for _ in range(self.w)] for _ in range(self.h)]

        image = Image.open(self.image_path)
        image = image.resize((self.w, self.h))  # Resize the image to the desired dimensions
        image = image.convert('L')  # Convert to grayscale

        pixel_data = list(image.getdata())

        ascii_chars = ['@', '#', '8', '&', '$', '%', 'O', '<bg>',"<bg>","<bg>","<bg>","<bg>","<bg>","<bg>","<bg>","<bg>","<bg>","<bg>","<bg>"]  # Expanded list

        for i, pixel_value in enumerate(pixel_data):
            row = i // self.w
            col = i % self.w

            # Map pixel value to ASCII character based on intensity
            char_index = int(pixel_value / 25.5)  # Adjusted calculation
            ascii_char = ascii_chars[char_index]

            custom_shape[row][col] = ascii_char

        return custom_shape



class Collider:
    def __init__(self):
        self.ids = []
        self.bounds = []

    def collider(self, obj, obj_id, offset=1):
        x, y, w, h = obj.x, obj.y, obj.w, obj.h

        matrix = []
        for i in range(h + offset):
            item = list(range(x - offset, x + w + offset))
            matrix.append((y + i - offset, item))

        for item in self.bounds:
            if obj_id == item[0]:
                self.bounds.remove(item)

        matrix = [obj_id, matrix]
        self.bounds.append(matrix)

        return self.check_for_collision(obj_id)

    def check_for_collision(self, obj_id):
        current = None
        rest = []

        for bound in self.bounds:
            if obj_id == bound[0]:
                current = bound[1]
            else:
                rest.append(bound[1])


        for item in current:
            for other_bounds in rest:
                for other_item in other_bounds:

                    if item[0] == other_item[0]:
                        if any(x in other_item[1] for x in item[1]):
                            collision_sides = self.get_sides_of_collision(item, other_item,current,other_bounds)
                            return collision_sides

        return None


    
    def get_sides_of_collision(self,item, other_item,bounds,other_bounds):
        sides = []


        #if bounds[-1][0]-1 < other_bounds[0][0]:
        #    sides.append("bottom")
        #if bounds[0][0]+1 > other_bounds[-1][0]:
        #    sides.append("top")
        #print(item[1])
        
        #correction = [x > other_item[1][0] for x in item[1]]
        #print(correction)
        #if correction[int(len(correction)/2)]:
        #    #if item[1][0] < other_item[1][-1]:
        #    sides.append('bottom')
        #if any(x < other_item[1][0]+1 for x in item[1][0:int(len(item[1])/2)]):
        #   sides.append('top')
        
        if any(x == other_item[1][0] - 1 for x in item[1]):
            sides.append('left')
        if any(x == other_item[1][-1] + 1 for x in item[1]):
            sides.append('right')


        #if "bottom" in sides and "left" in sides and "right" in sides:
        #    sides.pop(sides.index("left"))
        #    sides.pop(sides.index("right"))
        #if "top" in sides and "left" in sides and "right" in sides:
        #    sides.pop(sides.index("left"))
        #    sides.pop(sides.index("right"))
        #if "top" in sides and "left" in sides: sides.pop(sides.index("top"))
        #if "top" in sides and "right" in sides: sides.pop(sides.index("top"))

        return sides


class physics:
    def __init__(self,air_coefficient = 0.1,gravity_constant = 1.4):

        self.ac = air_coefficient
        self.gc = gravity_constant
    def force(self,force,mass,time):

        speed = (force/mass) * time
        speed = int(round(speed,1))
        if speed > 15: speed = 15
        if speed < -15: speed = -15

        return speed
    def air_resistance(self,speed):
        return speed * self.ac

    def gravity(self,time):
        out = 0.5 * self.gc * (time ** 2)
        return int(round(out,1))









def move_position(object : Robject,x = 0,y = 0):

    object.x = object.x + x
    object.y = object.y + y
    object.update(object.x,object.y)






class KeyboardHandler:
    def __init__(self):
        self.key_states = {}

    def register_key(self, key):
        self.key_states[key] = False

        # Register key press events
        keyboard.on_press_key(key, lambda _: self.set_key_state(key, True))

        # Register key release events
        keyboard.on_release_key(key, lambda _: self.set_key_state(key, False))

    def set_key_state(self, key, value):
        self.key_states[key] = value

    def is_key_pressed(self, key):
        if key in self.key_states:
            return self.key_states[key]
        return False




class Camera:
    def __init__(self,objects : list,x=0,y=0):
        self.objects = objects
        
        
        if x < 0 or y < 0:
            raise ValueError("x and y must be positive integers")
        self.x = x
        self.y = y
        self.update()
        
    def update(self):
        for object in self.objects:
            move_position(object, -self.x, -self.y)
            
            
    def register_object(self,object):
        self.objects.append(object)
        
        
keyboard_handler = KeyboardHandler()
keyboard_handler.register_key("a")
keyboard_handler.register_key("d")
keyboard_handler.register_key("s")
keyboard_handler.register_key("w")


#example use with other attributes:
renderer = Renderer(200,60,background=" ")





cube = Cube(renderer,12,6,filled=True)
cube.update(70,20)

cube_2 = Cube(renderer,5, 56,filled=True)
cube_2.update(195,0)
cube_3 = Cube(renderer,5,56,filled=True)
cube_3.update(0,0)
cube_4 = Cube(renderer,400,3,filled=True)
cube_4.update(0,57)

cube_6 = Cube(renderer,50,10,filled=True)
cube_6.update(80,50)
cube_5 = Cube(renderer,90,5,filled=True)
cube_5.update(70,30)
c= Collider()
camera = Camera([cube,cube_2,cube_3,cube_4,cube_5],50,50)
move_position(cube, 50, 50)
move_position(cube_2, 50, 50)
move_position(cube_3, 50, 50)
move_position(cube_4, 50, 50)
move_position(cube_5, 50, 50)



physics = physics(air_coefficient=0.1)

t = time.time()

force = 10
object_mass = 10
turn_on_grav = True
jumping = False
jump_start_time = 0
jump_duration = 0.5  # Adjust the jump duration as needed
jump_force = 70
gravityt = time.time()
jump_speed = 0



isgrounded = False
@Runtime
def update():

    # variables
    global object_mass, jump_speed
    global force
    global t
    global turn_on_grav
    global jumping
    global jump_start_time
    global jump_force
    global gravityt
    global isgrounded

    # start
    renderer.refresh()

    # defining controls
    if keyboard_handler.is_key_pressed("a"):
        t = time.time()
        force = -30
        camera.x = 25

    if keyboard_handler.is_key_pressed("d"):
        t = time.time()
        force = 30
        camera.x = 75

    if keyboard_handler.is_key_pressed("w") and isgrounded:
        print("pressing")
        jumping = True
        gravityt = time.time()
        jump_start_time = time.time()







    # defining collision

    collision = c.collider(cube, "1",offset=1)
    coll1 = c.collider(cube_2, "2",offset= 1)
    coll2 = c.collider(cube_3, "3",offset= 1)
    coll3 = c.collider(cube_4, "4",offset= 1)
    coll4 = c.collider(cube_5, "5", offset=1)


    #print(coll4)
    # collision rule
    #if coll1 is not None or coll2 is not None:
    if collision is not None:
        if "left" in collision:
            if force > 0:
                force = force * -1
            else:
                force = force
        if "right" in collision:
            if force < 0:
                force = force * -1
            else:
                force = force

    # applying force to the object



    current_time = time.time() - t + 1
    jp = time.time() - gravityt + 1.5
    sp = physics.force(force, object_mass, current_time)


    gravity = physics.gravity(jp)

    if jumping:
        jump_time = time.time() - jump_start_time
        if jump_time <= jump_duration:
            jump_speed = physics.force(jump_force, object_mass,jump_duration - jump_time)
              # Apply upward jump force
            jump_speed = jump_speed

        else:
            jumping = False
    isgrounded = False



    if collision is not None:
        if "top" in collision:
            jump_speed = 0
        if "bottom" in collision:
            isgrounded = True
            gravityt = time.time()
            gravity = 0


    #if coll3 != None:
    #    if "top" in coll3:
    #        gravityt = time.time()
    #        gravity = 0
    #        isgrounded = True

    if force < 2 and force > -2:
        force = 0

    # applying air resistance
    air_res = physics.air_resistance(sp)
    force -= air_res
    #print(coll4)
    print(collision)
    # apply the position
    #print(gravity)
    if turn_on_grav:
        f = jump_speed - gravity
        move_position(cube, sp,-f)

        if cube.y < 0:
            cube.y = 0
            
        
    else:
        move_position(cube, sp, 0)
    move_position(cube_2, 0, 0)
    move_position(cube_3, 0, 0)
    move_position(cube_4, 0, 0)
    move_position(cube_5, 0, 0)

    return renderer.draw_screen()#renderer.draw_screen()
