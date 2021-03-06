from Modules.Object.CustomObjects.GenericObject import GenericObject
import Modules.World
import pygame

class Decoration(GenericObject):
        def __init__(self, P, V, image):
                self.init_vectors()
                self.V = V
                self.P = P
                self.rect = image.get_rect()
                self.image = pygame.Surface((self.rect.w, self.rect.h), flags=pygame.HWSURFACE|pygame.SRCALPHA).convert_alpha()
                self.image.blit(image.convert_alpha(), (0,0))
                
                
        def static_blit(self):
                pass
        
        def draw(self, to):
                to.blit( self.image, (int(self.P[0]-self.rect.w/2), int(self.P[1]-self.rect.h/2)))
                #pass

