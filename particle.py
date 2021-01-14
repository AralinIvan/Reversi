import pygame.sprite
screen_rect = (0, 0, 800, 800)
all_sprites = pygame.sprite.Group()


class Particle(pygame.sprite.Sprite):


    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = pygame.image.load("data/star.png")
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.y > 800:
            self.kill()