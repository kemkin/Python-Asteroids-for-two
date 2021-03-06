from Modules.Object.CustomObjects.GenericObject import GenericObject
import Modules.World
import pygame

class Explosion(GenericObject):
        def __init__(self, P, sprite):
                self.P = P
                self.sprite = sprite
                self.killMe = False
                self.count = 0
                self.per_x_fps = 2
                
        def static_blit(self):
                pass
        
        def draw(self, to):
                if self.killMe == True:
                        Modules.World.world.remove_over(self)
                        
                self.count += 1
                
                img = self.sprite.current()
                if self.count%self.per_x_fps==0:
                        self.killMe = self.sprite.next()
                r = img.get_rect()
                position = (self.P[0]-r.w/2, self.P[1]-r.h/2)
                to.blit(img, position)
                 
        def collision(self, obj):
                '''
                On collision
                '''
                print ( "I'mma bullet and I've collided with da object1" )
                try:
                        Modules.World.world.remove_bullet(self)
                except ValueError:
                        pass
