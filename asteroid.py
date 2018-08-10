# RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def keydown (key):
    if key == simplegui.KEY_MAP["right"]:
       my_ship.angle_vel += 0.1
    elif key == simplegui.KEY_MAP["left"]:
       my_ship.angle_vel -= 0.1
    elif key == simplegui.KEY_MAP["up"]:
       my_ship.thrust = True
    elif key == simplegui.KEY_MAP["space"]:
       my_ship.shoot()

def keyup (key):
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust = False
    elif key == simplegui.KEY_MAP["space"]:
       pass

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self,canvas):
        if self.thrust :
            self.image_center[0] = 135
            ship_thrust_sound.play()
        else :
            self.image_center[0] = 45
            ship_thrust_sound.pause()
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def shoot (self):
        global missile_group, a_missile
        foward = angle_to_vector(self.angle)
        a_missile.pos[0] = self.pos[0] + foward[0] * self.image_size[0] / 2
        a_missile.pos[1] = self.pos[1] + foward[1] * self.image_size[1] / 2
        a_missile.vel[0] = self.vel[0] + (foward[0]*6)
        a_missile.vel[1] = self.vel[1] + (foward[1]*6)
        a_missile=Sprite(a_missile.pos, a_missile.vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def update(self):
        self.angle += self.angle_vel
        if self.thrust :
            vector = angle_to_vector(self.angle)
            self.vel[0] += vector[0] * .1
            self.vel[1] += vector[1] * .1
        self.pos = [(self.pos[0] +  self.vel [0])%WIDTH, (self.pos[1] + self.vel[1])%HEIGHT]
        self.vel = [self.vel [0]*0.99, self.vel [1]*0.99]
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):

        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        remove = False
        self.angle += self.angle_vel
        self.pos[0] =(self.pos[0] + self.vel[0])%WIDTH
        self.pos[1] = ( self.pos[1] + self.vel[1])%HEIGHT
        self.age = self.age + 1
        if self.age > self.lifespan:
           remove = True
        return remove

    def collide(self, other_object):
        min_dist = self.radius + other_object.get_radius()
        real_dist = dist(self.pos, other_object.get_pos())
        if real_dist < min_dist:
            return True
        else:
            return False
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

def draw(canvas):
    global time, started, lives, score, rock_group

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)


    # update ship and sprites
    my_ship.update()
    lives -= group_collide(rock_group, my_ship)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(missile_group, canvas)


    if group_collide(rock_group, my_ship) > 0:
        lives -= 1

    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())


def process_sprite_group(sprites, canvas):

    for sprite in set(sprites):
        sprite.draw(canvas)
        if sprite.update():
            sprites.remove(sprite)


def group_collide(group, other_object):
    collide = False
    num_collides = 0
    for i in set (group):
        if i.collide(other_object):
            num_collides += 1
            group.remove(i)

    return num_collides

# timer handler that spawns a rock
def rock_spawner():
    global rock_group
    vel = [random.randrange(-5,4), random.randrange(-5,4)]
    pos = [random.randrange(0,WIDTH), random.randrange(0,HEIGHT)]
    lower = 0.05
    upper = 0.2
    range_width = upper - lower
    ang_vel = random.random()* range_width + lower
    a_rock = Sprite (pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
    if len(rock_group) < 12 and started:
        if not a_rock.collide(my_ship):
            rock_group.add(a_rock)



# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
