import os
import random

import pygame

from DragonCard import DragonCard
from Tile import Tile
import math
from PlayerCard import PlayerCard
from Token import Token


class GameBoard:
    def __init__(self, card_images, card_back_image, tile_images, player_card_images, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.tile_images = tile_images[0]
        self.tile_images_animal = tile_images[1]
        self.cards = self.create_cards(card_images, card_back_image)
        self.tiles = self.create_tiles(tile_images)
        self.player_cards = self.create_player_cards(player_card_images)
        self.tokens = self.create_tokens()

    def shuffle_dragon_cards(self):
        # Shuffle the dragon cards and reset their flip status
        random.shuffle(self.cards)
        self.assign_new_positions()
        for card in self.cards:
            card.is_flipped = False

    def assign_new_positions(self):
        positions = self.calculate_positions(len(self.cards))
        for card, pos in zip(self.cards, positions):
            card.rect.topleft = pos  # Update card position

    def create_cards(self, card_images, card_back_image):
        positions = self.calculate_positions(len(card_images[0]))
        cards = [
            DragonCard(img, card_back_image, pos, animal)
            for img, pos, animal in zip(card_images[0], positions, card_images[1])
        ]

        random.shuffle(cards)
        return cards

    def create_tiles(self, tile_images):
        num_tiles = len(tile_images[0]) * 6
        positions = self.calculate_tile_positions(num_tiles)
        tiles = [Tile(img, pos, animal) for img, pos, animal in zip(tile_images[0] * 6, positions,tile_images[1]*6)]
        return tiles

    def create_player_cards(self, player_card_images):
        positions = self.calculate_player_card_positions()
        player_cards = [
            PlayerCard(img, pos, animal) for img, pos, animal in zip(player_card_images[0], positions,player_card_images[1])
        ]

        return player_cards

    def create_tokens(self):
        # Create four different colored tokens, one for each player card
        colors = [(128, 0, 128), (255, 255, 0), (173, 216, 230), (255, 192, 203)]
        token_size = (40, 40)  # Width and height of tokens
        tokens = []
        for color, pos in zip(colors, self.calculate_player_card_positions()):
            pc = None
            for x in self.player_cards:
                if x.position == pos:
                    pc = x
                    break
            tokens.append(Token(color, (pos[0] + 45, pos[1] + 55), token_size, pc))
        return tokens

    def update_tokens(self, selected_tokens):
        for index, token in enumerate(self.tokens):
            token.color = selected_tokens[index]
            token.image.fill(selected_tokens[index])  # Update the token color

    def calculate_positions(self, num_cards):
        positions = []
        cards_per_row = 4  # Adjust if necessary based on preference
        card_width = 60  # Card width
        card_height = 100  # Card height
        margin = 25  # Space between cards

        # Dynamically calculate starting positions based on screen size
        total_card_width = cards_per_row * (card_width + margin) - margin
        start_x = (self.screen_width - total_card_width) // 2
        start_y = (self.screen_height - (card_height + margin) * (
                (num_cards + cards_per_row - 1) // cards_per_row)) // 2

        for i in range(num_cards):
            row = i // cards_per_row
            col = i % cards_per_row
            x = start_x + col * (card_width + margin)
            y = start_y + row * (card_height + margin)
            positions.append((x, y))
        return positions

    def calculate_tile_positions(self, num_tiles):
        positions = []
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        radius = min(self.screen_width, self.screen_height) // 2.5  # Dynamic radius based on screen size

        angle_step = 360 / num_tiles

        for i in range(num_tiles):
            angle = math.radians(i * angle_step)
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            positions.append((x, y))
        return positions

    def calculate_player_card_positions(self):
        positions = []
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        # Get positions of the 4 corners of the circle of 24 tiles
        tile_positions = self.calculate_tile_positions(24)
        corner_positions = [
            tile_positions[i * 6] for i in range(4)
        ]  # Every 6th tile position is a corner position

        offset = 450  # Distance of player cards from the middle
        angle_shift = math.radians(45)  # Angle to shift for each player card

        for _, corner_pos in enumerate(corner_positions):
            x, y = corner_pos
            # Calculate the angle from the center of the circle to the corner position
            angle_to_corner = math.atan2(y - center_y, x - center_x)
            # Shift the angle by 45 degrees
            shifted_angle = angle_to_corner + angle_shift
            # Calculate the position of the player card using polar coordinates
            card_x = center_x + int(offset * math.cos(shifted_angle))
            card_y = center_y + int(offset * math.sin(shifted_angle))
            positions.append((card_x, card_y))

        return positions

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        for card in self.cards:
            card.draw(surface)
            for player_card in self.player_cards:
                player_card.draw(surface)
                for token in self.tokens:
                    token.draw(surface)
