class Tile:
    def __init__(self, image, position, animal):
        self.is_flipped = None
        self.image = image
        self.rect = image.get_rect(center=position)
        self.animal = self.what_animal(animal)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def flip(self):
        self.is_flipped = not self.is_flipped

    def what_animal(self, animal):
        if animal == "babyDragonVolcanoCard":
            return "Dragon"
        elif animal == "batVolcanoCard":
            return "Bat"
        elif animal == "salamanderVolcanoCard":
            return "Salamander"
        elif animal == "spiderVolcanoCard":
            return "Spider"


