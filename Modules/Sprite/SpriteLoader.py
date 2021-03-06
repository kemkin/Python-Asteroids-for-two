from Modules.Config.Config import ConfigReader2
from Modules.Config import get
import Modules.Object.Loader
import pygame

class SpriteLoader():
        def __init__(self):
                self.cached = dict()
                
        def load_config(self, name):
                cfg = ConfigReader2("{0}/{1}/{2}{3}".format(get("Objects"), get("Sprite Config Path"), name, get("Sprite Config Suffix")))
                path="{0}/{1}{2}".format(get("Sprite Image Path"), name, get("Sprite Image Suffix"))
                print (path)
                image = Modules.Object.Loader.load_images([['default',path]])['default']
                images = dict()
                surname = ""
                for sett in cfg.settings:
                        s = sett[0]
                        if s == "Sprite":
                                surname = sett[1]
                                images[surname] = []
                        elif s == "Picture":
                                c = sett[1].split(" ")
                                r = pygame.Rect ( int(c[0]), int(c[1]), int(c[2]), int(c[3]) ) 
                                
                                surface = pygame.Surface( (r.w, r.h), pygame.SRCALPHA ).convert_alpha()
                                surface.blit( image, (-r.x, -r.y) )
                                images[surname] += [surface]
                return images
                
        def load(self, name, surname, scale):
                images = self.load_config(name)
                images_in_surname = images[surname]
                print (images)
                for i in range(0, len(images_in_surname)):
                        img = images_in_surname[i]
                        r = img.get_rect()
                        images_in_surname[i] = pygame.transform.scale(images_in_surname[i], (int(r.w*scale), int(r.h*scale))).convert_alpha()
                return  images[surname]
                
singleton = SpriteLoader()
