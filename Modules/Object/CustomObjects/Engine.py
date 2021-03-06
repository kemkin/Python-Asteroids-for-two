'''
02.12.2010 Andrej Cizov

Engine class
'''
import Modules.World
import pygame
from Modules.Vector25D import Vector25D
from Modules.Vector25D import rotate_around_point
from Modules.Object.CustomObjects.GenericObject import GenericObjectPart
import math

class Engine(GenericObjectPart):
        def init(self): 
                self.working = False
        
        def init_custom_info(self, custom):
                self.acceleration = float(custom['Acceleration'])
                p = custom['Acceleration Position'].split(" ")
                self.A = Vector25D(math.sin(self.pos[2]/180*math.pi), math.cos(-self.pos[2]/180*math.pi))*self.acceleration*-1
                
        def init_after_parent(self):
                self.P = self.parent.center_of_mass-(self.pos+Vector25D(self.rect.w/2, self.rect.h/2))     
  
        def accelerate_start(self, c):
                self.working = True
                #print ("Acceleration of {0} with coefficient {1}".format(self.acceleration, c))
                F = self.A*c
                F = (F).rotate(-self.parent.P[2])
                P = (self.P).rotate(-self.parent.P[2])
                F.v[2] = 0
                P.v[2] = 0
                Modules.World.world.physics.apply_force( self.parent, F, P )
                
        def accelerate_stop(self):
                self.working = False
                
        def get_controls(self):
                return [Engine.accelerate_start, Engine.accelerate_stop]
                
        def static_redraw(self):
                        self.blit_static(self.images['Stall'])
                
        def dynamic_redraw(self):
                '''
                Better to do it in parent object!!!
                '''
                if self.working == True:
                        self.blit_dynamic(self.images['Running'])
