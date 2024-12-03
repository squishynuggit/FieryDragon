import pygame


class PlayerCard:
    def __init__(self, image, position, animal):
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(center=position)
        self.animal = self.what_animal(animal)
        self.empty = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def what_animal(self, animal):
        if animal == "babyDragonInCave":
            return "Dragon"
        elif animal == "batInCave":
            return "Bat"
        elif animal == "salamanderInCave":
            return "Salamander"
        elif animal == "spiderInCave":
            return "Spider"
