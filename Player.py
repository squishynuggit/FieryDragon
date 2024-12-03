
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  # Assuming players have a hand of cards
        self.score = 0  # If your game involves scoring

    @staticmethod
    def flip_card(card):
        # Assume 'card' is an instance of DragonCard
        card.flip()

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def remove_card_from_hand(self, card):
        self.hand.remove(card)

    def update_score(self, points):
        self.score += points
