import arcade
import room_setup
import numpy as np
from numpy import linalg as LA
import math
import sound_manager
import game

GOBLIN = 0
HOBGOBLIN = 1

class Goblin():

    def __init__(self,  health = 4, damage = 2, armor = 0, center_x = 0, center_y = 0, attack_range = 45, gobtype=GOBLIN, movespeed = 3):
        self.health = health
        self.damage = damage
        self.armor = armor
        self.x = center_x
        self.y = center_y
        self.movespeed = movespeed
        self.attack_cooldown = 0
        self.attack_range = attack_range
        self.type = gobtype
        

    def die(self, room, left, bottom):
        blood_splatter = arcade.Sprite("resources/images/blood.png", .7)
        blood_splatter.left = left
        blood_splatter.bottom = bottom
        room.accent_list.append(blood_splatter)
        if self.type == GOBLIN:
            sound_manager.play_sound(sound_manager.GOBLIN_DEATH, .15)
        else:
            sound_manager.play_sound(sound_manager.HOBGOBLIN_DEATH, .15)
            arcade.window_commands.pause(1.5)


    def take_damage(self, damage):
        damage -= 1
        dealt = damage - self.armor
        self.health -= 1
        if dealt > 0:
            self.health -= dealt

    def update(self, slayer_position, room, sprite):
        self.x = sprite.center_x
        self.y = sprite.center_y
        self.attack_cooldown -= 1
        if arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list) and not arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list, self.attack_range):
            if slayer_position[0] - (self.x, self.y)[0] <= -6:
                sprite.change_x = -self.movespeed
            elif slayer_position[0] - (self.x, self.y)[0] >= 6:
                sprite.change_x = self.movespeed
            else:
                sprite.change_x = 0
            if slayer_position[1] - (self.x, self.y)[1] <= -6:
                sprite.change_y = -self.movespeed
            elif slayer_position[1] - (self.x, self.y)[1] >= 6:
                sprite.change_y = self.movespeed
            else:
                sprite.change_y = 0
        if arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list, 50):
            if sprite.change_x != 0:
                sprite.change_x = 0
            if sprite.change_y != 0:
                sprite.change_y = 0
            if self.attack_cooldown <= 0:
                spawn_x = self.x
                spawn_y = self.y
                connect_vector = [slayer_position[0] - spawn_x, slayer_position[1] - spawn_y]
                connect_vector = connect_vector / LA.norm(connect_vector)
                angle = math.degrees(np.arccos(connect_vector)[0])
                if slayer_position[1] < spawn_y:
                    angle = -angle
                connect_vector = np.multiply(connect_vector, self.attack_range)
                spawn_vector = np.add(connect_vector, [spawn_x, spawn_y])
                room_setup.add_enemy_attack(room, spawn_vector[0], spawn_vector[1], angle, self.damage)
                if self.type == GOBLIN:
                    self.attack_cooldown = 20
                    sound_manager.play_sound(sound_manager.GOBLIN_ATTACK, .15)
                else:
                    self.attack_cooldown = 45
                    sound_manager.play_sound(sound_manager.HOBGOBLIN_ATTACK, .15)
        
        