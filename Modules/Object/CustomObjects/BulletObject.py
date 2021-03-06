from Modules.Object.CustomObjects.GenericObject import GenericObject
from Modules.Vector25D import Vector25D
from Modules.Config import get
import Modules.World
import pygame

DAMAGEMULT=float(get("Bullet Damage Multiplier"))
BULLETLIFESPAN=int(get("Bullet Lifespan"))

class Bullet(GenericObject):
        def __init__(self, P, V, r, color, mass):
                global BULLETLIFESPAN
                self.HP = 100
                self.init_vectors()
                self.V = V
                self.P = P
                self.mass = mass
                self.r = 4
                self.color = color
                self.rect = pygame.Rect( (P[0]-r/2, P[1]-r/2), (r/2, r/2) )
                self.lifespan = BULLETLIFESPAN
                self.mask = pygame.mask.Mask((1,1))
                self.mask.set_at((0,0), True)
                
        def static_blit(self):
                pass
        
        def draw(self, to):
                self.rect.x = self.P[0]-self.r/2
                self.rect.y = self.P[1]-self.r/2
                try:
                        pygame.draw.circle(to, self.color, (int(self.P[0]), int(self.P[1])), self.r)
                except OverflowError:
                        pass
                self.lifespan-=1
                if self.lifespan == 0:
                        Modules.World.world.remove_bullet(self)
                        
        def show_damage(self, n):
                pass
                 
        def collision(self, obj):
                '''
                On collision
                '''
                self.damage(self.HP)
                Modules.World.world.bullet_explosion(self.P)
                Modules.World.world.physics.apply_force(obj, self.V*self.mass**3, obj.P-self.P)
                global DAMAGEMULT
                obj.damage(self.V.length()*DAMAGEMULT*self.mass)
                

        def destroy(self): 
                Modules.World.world.remove_bullet(self)
                
                
                
