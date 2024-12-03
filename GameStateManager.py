import os
import json


class GameStateManager:
    def __init__(self, game):
        self.game = game

    @staticmethod
    def list_save_files():
        """List all save files in the current directory."""
        return [f for f in os.listdir() if f.endswith('.json')]

    def delete_save_file(self, filename):
        os.remove(filename)

    def save_game(self, filename):
        """Save the game state to a file with the given filename."""
        game_data = {
            "volcanoCards": [
                {
                    "cardType": tile.animal,
                    "cave": hasattr(tile, 'cave'),
                    "animalOnTile": tile.animal,
                    "position": index
                } for index, tile in enumerate(self.game.board.tiles)
            ],
            "playerTokens": [
                {
                    "playerId": index + 1,
                    "tokenColor": str(token.color),
                    "position": self.game.token_pos[index],
                    "stillInCave": token.still_in_cave
                } for index, token in enumerate(self.game.board.tokens)
            ],
            "dragonCards": [
                {
                    "cardType": card.animal,
                    "isFlipped": card.is_flipped,
                    "position": self.game.board.cards.index(card)
                } for card in self.game.board.cards
            ],
            "gameState": {
                "currentPlayerTurn": self.game.player_in_turn,
                "sequenceOfPlay": list(range(1, self.game.number_of_player + 1))
            }
        }
        with open(filename, 'w') as file:
            json.dump(game_data, file, indent=4)

    def load_game(self, filename):
        """Load the game state from a file with the given filename."""
        with open(filename, 'r') as file:
            game_data = json.load(file)

            for index, card_data in enumerate(game_data["volcanoCards"]):
                tile = self.game.board.tiles[index]
                tile.animal = card_data["animalOnTile"]
                if 'cave' in card_data and card_data['cave']:
                    tile.cave = True

            for token_data in game_data["playerTokens"]:
                index = token_data["playerId"] - 1
                token = self.game.board.tokens[index]
                token.color = token_data["tokenColor"]
                token.still_in_cave = token_data["stillInCave"]
                if token_data["stillInCave"]:
                    token.currently_on = token.player_c
                else:
                    token.currently_on = self.game.board.tiles[token_data["position"]]
                self.game.token_pos[index] = token_data["position"]

            for card_data in game_data["dragonCards"]:
                card = self.game.board.cards[card_data["position"]]
                card.animal = card_data["cardType"]
                card.is_flipped = card_data["isFlipped"]

            self.game.player_in_turn = game_data["gameState"]["currentPlayerTurn"]
            self.game.sequence_of_play = game_data["gameState"]["sequenceOfPlay"]
            self.game.state = 'GAME'  # Set game state to 'GAME'
            self.game.game_active = True  # Set game as active
