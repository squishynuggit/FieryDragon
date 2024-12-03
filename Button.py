# button.py
import pygame


class Button:
    def __init__(self, text, x, y, width, height, font, color, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.color = color
        self.callback = callback  # The method to call when the button is clicked
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, surface):
        # Draw the button rectangle
        pygame.draw.rect(surface, self.color, self.rect)
        # Draw the button text
        text_surf = self.font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()  # Call the button's callback method
