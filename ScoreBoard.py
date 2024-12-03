import pygame

from Button import Button


def readScores():
    scores = []
    try:
        with open('scores.txt', 'r') as file:
            for line in file:
                number = int(line.strip())
                scores.append(number)
    except Exception:
        print("")
    return scores


def saveScore(player):
    scores = readScores()
    scores[player] += 1
    with open('scores.txt', 'w') as file:
        for score in scores:
            file.write(str(score) + "\n")


class ScoreBoard:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.backBtn = Button(
            'Back', 50, 50, 150, 60,
            self.font, (0, 200, 0), None
        )
        self.scores = readScores()

    def active(self, screen):
        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backBtn.rect.collidepoint(event.pos):
                        return

            screen.fill((0, 0, 0))
            self.backBtn.draw(screen)

            x = 1280 / 2 - 30
            y = 200
            i = 1
            for score in self.scores:
                text_surface = self.font.render(f"player {i} : {score} wins", False, (233, 233, 233))
                screen.blit(text_surface, (x, y))
                i += 1
                y += 50

            pygame.display.flip()
