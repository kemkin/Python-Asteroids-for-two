'''
02.12.2010 written by Andrej Cizov

Game world module. Registers objects in the game

this module 
- manages the interaction of objects
- registers it in the interaction modules
- manages the input so that every object would receive it's input correctly
'''
from Modules.Config import get
import Modules.Object.Loader
from Modules.Vector25D import Vector25D
import pygame
from pygame.locals import *
import Modules.Physics
from Modules.Object.CustomObjects.BulletObject import Bullet
from Modules.Object.CustomObjects.DecorationObject import Decoration
from Modules.Object.CustomObjects.Explosion import Explosion
from Modules.Object.CustomObjects.Asteroid import Asteroid

from Modules.Sprite.Sprite import Sprite

import Modules.Sprite.SpriteLoader

from Modules.Input import Input

import random

print ( "iii Loading game world module!" )

'''
Do some world classes here
'''

DRAW_FONTS = True

class World():
        def __init__(self):
                self.dimensions = ( int(get("Window Width")), int(get("Window Height")) )
                
                pygame.init()
                
                self.init_screen()
                self.init_background()
                self.init_physics()
                
                self.init_explosions()
                self.init_fonts()
                
                # 1 Objects under the standart objects
                self.fast_objects = []
                
                # 2 Standart obejcts
                self.objects = []
                
                # 3 Objects over the standart objects
                self.over_objects = []
                
                # 4 Texts which we want to show
                self.texts = []
                
                # 5 Interface objects we're blitting to the screen
                self.interfaces = []
                
                
                self.clock = pygame.time.Clock()
                
                self.fps = int(get("FPS"))
                
                self.tickcount = 0
                self.input = Input()
                
                self.stop = False
                
                self.global_mappings = GlobalKeyMappings(self)
                
        @staticmethod
        def font(name):
                # return pygame.font.Font(pygame.font.match_font(get("Font {0}".format(name))), int(get("Font {0} Size".format(name))))
                n,s = get("Font {0}".format(name)), int(get("Font {0} Size".format(name)))
                print('iii Loading Font {}, Size={}'.format(n,s))
                r = pygame.font.Font(pygame.font.match_font(n), s)
                #r = None
                #r = pygame.font.Font(pygame.font.match_font(None, s))
                print('iii Loaded Font {}, Size={}'.format(n,s))
                return r 
                
        def init_fonts(self):
                pygame.font.init()
                self.font_HP = self.font("HP")
                self.font_info = self.font("Info")
                self.font_fastinfo = self.font("FastInfo")
                
        def add_over(self, obj):
                self.over_objects+=[obj]
                
        def remove_over(self, obj):
                try:
                        self.over_objects.remove(obj)
                except ValueError:
                        pass
                
        def physics_add(self, obj, modules):
                for i in modules:
                        self.physics[i].add(obj)
                        
        def physics_remove(self, obj, modules):
                for i in modules:
                        self.physics[i].remove(obj)
                
        def add_decoration(self, P, V, path):
                image = Modules.Object.Loader.load_images([['default',path]])['default']
                obj = Decoration(P, V, image)
                self.physics_add(obj, self.physics_decoration_modules)
                self.fast_add(obj)
                
        def add_bullet(self, P, V, r, color, mass):
                obj = Bullet(P, V, r, color, mass)
                # Collisions Moving and ScreenLoop 
                self.physics_add(obj, self.physics_bullet_modules)
                self.fast_add(obj)
                
        def remove_bullet(self, obj):
                self.physics_remove(obj, self.physics_bullet_modules)
                try:
                        self.fast_remove(obj)   
                except ValueError:
                        pass 
                
        def fast_add(self, obj, physics_modules=None):
                if physics_modules:
                        self.physics_add(obj, physics_modules)
                self.fast_objects.append(obj)
                
        def fast_remove(self, obj, physics_modules=None):
                if physics_modules:
                        self.physics_remove(obj, physics_modules)
                try:
                        self.fast_objects.remove(obj)
                except ValueError:
                        pass
                
        def add(self, obj, physics_modules=None):
                if physics_modules == None:
                        physics_modules = self.physics_object_modules
                obj.blit_static()
                self.objects.append(obj)
                for i in physics_modules:
                                self.physics[i].add(obj)
                
        def remove(self, obj):
                try:
                        self.objects.remove(obj)
                        for i in self.physics_object_modules:
                                self.physics[i].remove(obj)
                except ValueError:
                        pass
                        
        def add_interface(self, obj):
                self.interfaces.append(obj)     
                
        def remove_interface(self, obj):
                try:
                        self.interfaces.remove(obj)
                except ValueError:
                        pass
                        
        def add_text(self, text, obj, scaleV, seconds, V = Vector25D()):
                '''
                Show short text message for a user
                text - what text to show
                obj - to what object the position of a text is related
                scaleV - scaleVelocity -> how much to scale the text on each frame
                seconds - how many seconds to show the text
                '''
                frames_to_live = seconds*self.fps
                
                if DRAW_FONTS:
                    self.texts.append([ self.font_fastinfo.render(text, True, (123,34,12)).convert_alpha(), obj, scaleV, frames_to_live, 0, V ])
                
        def remove_text(self, obj):
                self.texts.remove(obj)
                
        def self_draw_font(self, font, text, color, P, flags=0):
                World.draw_font(self.background, font, text, color, P, flags)
        @staticmethod        
        def draw_font(surf_to, font, text, color, P, flags=0):
                if DRAW_FONTS:
                    surf = font.render(text, True, color).convert_alpha()
                    r = surf.get_rect()
                    surf_to.blit(surf, (int(P[0]-r.w/2), int(P[1]-r.h/2)), special_flags=flags)
        
        def redraw(self):
                #self.background.blit(self.background_image, (0,0))
                self.background.fill ( (0,0,0, 255) )
                
                counter = 0
                
                for obj in self.fast_objects:
                        obj.draw(self.background)
                        counter+=1
                
                for obj in self.objects:
                        obj.draw(self.background)
                        counter+=1
                        
                for obj in self.over_objects:
                        obj.draw(self.background)
                        counter+=1
                        
                for obj in self.objects:
                        # Drawing font info here
                        self.self_draw_font(self.font_HP, str(int(obj.HP)), (255,255,255), obj.P+Vector25D(0,30))
                        counter+=1
                
                i = 0        
                for text in self.texts:
                        r = text[0].get_rect()
                        scale_factor = 1/text[2]**text[4]
                        blit_font = pygame.transform.scale( text[0], (int(r.w*scale_factor), int(r.h*scale_factor)))
                        r = blit_font.get_rect()
                        passed = text[4]/text[3]
                        self.background.blit(blit_font, (int(text[1].P[0] - r.w/2 + text[5][0]*passed), int(text[1].P[1] - r.h/2 + text[5][1]*passed)) )
                        self.texts[i][4]+=1
                        if (self.texts[i][4] > self.texts[i][3]):
                                self.remove_text(text)
                        i+=1
                        counter+=1
                        
                for obj in self.interfaces:
                        obj.draw(self.background)
                        counter+=1
                                
                #self.self_draw_font(self.font_info, "FPS: "+str(self.clock.get_fps()), (255,255,255), (800,100))
                #self.self_draw_font(self.font_info, "Fast object count: "+str(len(self.fast_objects)), (255,255,255), (1000,500))
                #self.self_draw_font(self.font_info, "Overall draw function calls: "+str(counter), (255,255,255), (1000,600))
                        
                self.screen.blit(self.background, (0,0))
                pygame.display.flip()
                
        def init_explosions(self):
        	self.explosion_bomb = Modules.Sprite.SpriteLoader.singleton.load ( "SkybusterExplosion", "First", 1 ) 
        	self.explosion_bullet = Modules.Sprite.SpriteLoader.singleton.load ( "BlueExplosion", "First", 1 )
        	self.explosion_ship = Modules.Sprite.SpriteLoader.singleton.load ( "RedExplosion", "First", 1 )
        	
        def asteroid(self, P, V):
                asteroid = Modules.Object.Loader.load("GenericAsteroid", Asteroid)
                asteroid.P = P
                asteroid.V = V
                self.add(asteroid)
                self.fast_add(asteroid, self.physics_bullet_modules)
                return asteroid
        
        def explosion(self, sprite, P):
                e = Explosion(P, sprite)
                self.add_over(e)
        	
        def bomb_explosion(self, P):
                self.explosion ( Sprite( self.explosion_bomb, random.random()*360), P )
                
        def bullet_explosion(self,P):
        	self.explosion ( Sprite( self.explosion_bullet, random.random()*360), P )
        	
        def ship_explosion(self, P):
                self.explosion ( Sprite( self.explosion_ship, random.random()*360 ), P )
                
        def init_background_image(self, path):
                img = Modules.Object.Loader.load_images([['default',path]])['default']
                img = pygame.transform.scale( img, self.dimensions )
                self.background_image = img
                
        def loop(self, times):
                for i in range(0, times):
                        self.clock.tick(self.fps)
                        #self.clock.tick()
                        self.tickcount+=1
                        self.input.tick()    
                        self.redraw()
                        self.physics.tick()
                        
                        if self.stop:
                                return False 
                       
                return True
                
        def flush(self):
                self.fast_objects = []
                self.objects = []
                self.over_objects = []
                self.texts = []
                self.interfaces = []
                
                for phys in self.physics:
                        phys.flush()
                        
        def init_screen(self):
                pygame.init()
                dims = self.dimensions
                opts = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
                opts = pygame.DOUBLEBUF | pygame.HWSURFACE

                self.screen = pygame.display.set_mode((dims[0], int(dims[1])), opts)
                pygame.display.set_caption( get("Game Name") )
                
        def init_background(self):
                self.background = pygame.Surface(self.dimensions)
                self.init_background_image('./default.jpg')
                
        def get_all_indexes(self, name):
                module_names = get("Physics Modules "+name).split(" ")
                r = []
                for module in module_names:
                        r+=[self.physics.get_module_index(module)]
                return r
                
        def init_physics(self):
                #Gravity Collisions Acceleration Moving ZeroAcceleration ScreenLoop
                self.physics = Modules.Physics.Physics(self)
                self.physics_bullet_modules = self.get_all_indexes ( "Bullets" )
                self.physics_decoration_modules = self.get_all_indexes ( "Decorations" )
                self.physics_object_modules = self.get_all_indexes ( "Objects" )
                
class GlobalKeyMappings():
        def __init__(self, world):
                self.world = world
                self.init_map()
                self.parent = None
                
        def init_map(self):
                self.world.input.add_key_to_reaction( 27, [{'part_obj': self, 'coefficient': 3 }] )
                
        def get_controls(self):
                return [GlobalKeyMappings.esc_pressed, GlobalKeyMappings.esc_unpressed]
                
        def esc_pressed(self, c):
                self.world.stop = True
                
        def esc_unpressed(self):
                pass
                
world = World()

