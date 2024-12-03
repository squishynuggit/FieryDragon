import pygame
from PlayerCard import PlayerCard


class Token:
    def __init__(self, color, position, size, pc: PlayerCard):
        self.color = color
        self.position = position
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.player_c = pc
        self.currently_on = pc
        self.still_in_cave = True

    def draw(self, surface):
        surface.blit(self.image, self.currently_on.rect.center)
