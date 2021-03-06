import Modules.World
import pygame
from Modules.Vector25D import Vector25D

from Modules.Object.CustomObjects.GenericObject import GenericObjectPart
from Modules.Object.CustomObjects.GenericBomb import GenericBomb
import Modules.World
import Modules.Object.Loader
import math

class Bomber(GenericObjectPart):
        def init(self): 
                pass
        
        def init_custom_info(self, custom):
                self.blast_radius = float(custom['Blast Radius'])
                self.init_bomb_class(str(custom['Bomb Class']))
                self.bomb_name = str(custom['Bomb Name'])
                self.bomb_power = float(custom['Bomb Power'])
                self.bomb_timeout = float(custom['Bomb Timeout'])
                self.counter = 0
        
        def init_bomb_class(self, class_name):
                self.bomb_class = Modules.Object.Loader.load_object_class(class_name)
                
                
        def shoot_start(self, c):
                '''
                Create a bomb here
                '''
                if self.counter < 50:
                        self.counter+=1
                else:
                        bomb = Modules.Object.Loader.load(self.bomb_name, self.bomb_class)
                        bomb.set_radius(self.blast_radius)
                        bomb.set_power(self.bomb_power)
                        bomb.set_counter(self.bomb_timeout)
                        bomb.P = self.parent.P
                        Modules.World.world.add(bomb)
                        self.counter = 0
        
        def shoot_stop(self):
                self.counter = 0
                pass
                
        def get_controls(self):
                return [Bomber.shoot_start, Bomber.shoot_stop]

