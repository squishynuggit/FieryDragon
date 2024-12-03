import pygame


class DragonCard:
    def __init__(self, front_img, back_img, position, animal):
        self.front_img = front_img
        self.back_img = back_img
        self.is_flipped = False
        self.rect = front_img.get_rect(topleft=position)
        self.number, self.animal = self.what_animal(animal)

    def draw(self, surface):
        if self.is_flipped:
            surface.blit(self.front_img, self.rect)
        else:
            surface.blit(self.back_img, self.rect)

    def flip(self):
        self.is_flipped = not self.is_flipped

    def what_animal(self, animal):
        a = ["oneBabyDragon", "twoBabyDragon", "threeBabyDragon"]
        b = ["oneBat", "twoBat", "threeBat"]
        c = ["oneSalamander", "twoSalamander", "threeSalamander"]
        d = ["oneSpider", "twoSpider", "threeSpider"]
        e = ["onePirateDragon", "twoPirateDragon", "threePirateDragon"]
        if animal in a:
            for x in range(len(a)):
                if animal == a[x]:
                    return x + 1, "Dragon"
        elif animal in b:
            for x in range(len(b)):
                if animal == b[x]:
                    return x + 1, "Bat"
        elif animal in c:
            for x in range(len(c)):
                if animal == c[x]:
                    return x + 1, "Salamander"
        elif animal in d:
            for x in range(len(d)):
                if animal == d[x]:
                    return x + 1, "Spider"
        elif animal in e:
            for x in range(len(e)):
                if animal == e[x]:
                    return x + 1, "Pirate"
        elif animal == "PullBackToCave":
            return None, animal


