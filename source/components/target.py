import pygame
from .. import tools, setup

class Target(pygame.sprite.Sprite):
    def __init__(self, shape):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'target'
        self.shape = shape
        self.direction = 'right'
        self.state = 'stand'
        self.frame_index = 0
        self.frame_rects = [(90, 90, 15, 23)]  # , (144, 0, 15, 30)
        self.timer = 0
        self.load_frames()
        self.update()
        self.rect = self.image.get_rect()

    def stand(self):
        self.state = 'stand'

    def walk(self):
        self.state = 'walk'

    def left(self):
        self.direction = 'left'

    def right(self):
        self.direction = 'right'

    def load_frames(self):
        sheet = setup.GRAPHICS['smb_enemies_sheet']
        self.right_frames = []
        self.left_frames = []
        for frame_rect in self.frame_rects:
            right_image = tools.get_image_with_shape(sheet, *frame_rect, (0, 0, 0), self.shape)
            left_image = pygame.transform.flip(right_image, True, False)
            self.right_frames.append(right_image)
            self.left_frames.append(left_image)

    def update(self):
        if self.direction == 'left':
            # if self.state == 'stand':
            self.frames = [self.left_frames[0]]
            # else:
            #     self.frames = [self.left_frames[0], self.left_frames[1], self.left_frames[2]]
        elif self.direction == 'right':
            # if self.state == 'stand':
            self.frames = [self.right_frames[0]]
            # else:
            #     self.frames = [self.right_frames[0], self.right_frames[1], self.right_frames[2]]

        self.current_time = pygame.time.get_ticks()
        frame_durations = [100] * len(self.frames)

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= len(self.frames)
            self.timer = self.current_time

        self.image = self.frames[self.frame_index]



