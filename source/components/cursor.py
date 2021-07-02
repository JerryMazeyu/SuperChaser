import pygame
from .. import tools, setup
from .. import constants as C

class Cursor(pygame.sprite.Sprite):
    def __init__(self, frames, position):
        pygame.sprite.Sprite.__init__(self)
        self.is_active = True
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.timer = 0

    def activate(self):
        self.is_active = True

    def deactive(self):
        self.is_active = False

    def update_image(self):
        if self.is_active:
            self.current_time = pygame.time.get_ticks()
            frame_durations = [400]*len(self.frames)
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > frame_durations[self.frame_index]:
                self.frame_index += 1
                self.frame_index %= len(self.frames)
                self.timer = self.current_time
        else:
            self.frame_index = 0
        self.image = self.frames[self.frame_index]

class MushroomCursor(Cursor):
    def __init__(self, position=(260, 480)):
        mushroom_images = []
        for _ in range(3):
            tmp = pygame.Surface((30, 30))
            tmp.set_colorkey((0, 0, 0))
            mushroom_images.append(tmp)
        images = [tools.get_image(setup.GRAPHICS['item_objects'], 288, 2, 17, 14, (0, 0, 0), x) for x in [1, 1.2, 1.4]]
        for ind,img in enumerate(images):
            rect = img.get_rect()
            rect.centerx = 15
            rect.centery = 15
            mushroom_images[ind].blit(img, rect)
        super(MushroomCursor, self).__init__(mushroom_images, position)
        self.states = 'up'

    def update(self, keys):
        Cursor.update_image(self)
        if self.is_active:
            if keys[pygame.K_UP]:
                self.states = 'up'
            elif keys[pygame.K_DOWN]:
                self.states = 'down'



