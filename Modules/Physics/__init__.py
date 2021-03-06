'''
Created by Andrej Cizov 03.12.2010

Physics operation module
- detects collisions
- does force application to the main object
'''
from __future__ import absolute_import

from Modules.Register import Register
from Modules.Config import get


from Modules.Vector25D import Vector25D
import math
import random

BLAST_FORCE_MULT=float(get("Blast Force Multiplier"))
BLAST_DAMAGE_MULT=float(get("Blast Damage Multiplier"))

class Physics(Register):
        def __init__(self, world):
                Register.__init__(self)
                self.world = world
                self.init_modules () 
                print ("iii Modules.Physics loaded modules: {0}".format(self.items()))
                self.init_config()
        
        def init_modules(self):
                modules_list = get("Physics Modules").split(" ")
                self.class_list = dict()
                i = 0
                for module in modules_list:
                        self.load_module(module)
                        self.class_list[module] = i
                        i+=1
                        #
        def get_module_index(self, mod):
                return self.class_list[mod]
                        
        def init_config(self):
                self.pps = float(get("pps"))
                
        def apply_force(self, obj, F, P):
                '''
                applies force F to a point P of GenericObject obj
                
                P must be according to the obj's center of mass
                '''
                # getting the normal from point to the center of mass
                N = P #.norm()
                
                # The cross product of two vectors
                degr = P.cross(F)[2]/obj.I
                # angular part of the acceleration
                angular = degr/math.pi*180
                # linear part of the acceleration
                linear = F/(obj.mass)
                obj.A += linear+Vector25D(0,0,angular)
                
        def blast(self, P, r, strength):
                '''
                P - blast position
                strength - blast strength
                '''
                
                objects_in_radius = []
                for obj in self.world.objects:
                        if (P-obj.P).length2() < r:
                                objects_in_radius+=[obj]
                
                '''n = int(strength)
                for i in range(0, n):
                        V = Vector25D(1)
                        V = V.rotate(360/n*i)
                        self.world.add_bullet( P, (V*0.25+V*random.random())*(strength*strength), 3, (234, 0, 0), strength )'''
                               
                for obj in objects_in_radius:
                                F = (P-obj.P)
                                if (F.length2() == 0):
                                        F=Vector25D(strength,strength)
                                F = F/F.length2()*F.length2()
                                self.apply_force(obj, F*strength*BLAST_FORCE_MULT*-1, Vector25D())
                                obj.damage((math.sqrt(r)-F.length())*BLAST_DAMAGE_MULT*strength)
                pass
                        
        def load_module(self, name):
                module_path = "Modules.Physics."+name
                print (module_path)
                print ( "iii Modules.Physics loading module: '{0}'".format(module_path))
                m = __import__(module_path, {}, {}, [name])
                module_class = getattr(m, name)
                new_module = module_class(self.world)
                self.add(new_module)
                
                # Sets up basic information for the module
                new_module.parent = self
                
        def tick(self):
                for module in self.items():
                        module.tick()
                
