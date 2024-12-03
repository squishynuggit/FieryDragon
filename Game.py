import pygame
import os
from GameBoard import GameBoard
from Button import Button
from GameStateManager import GameStateManager
from ScoreBoard import saveScore


def play_background_music(music_file):
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error playing music: {e}")


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.state_manager = GameStateManager(self)
        self.card_width, self.card_height = 100, 150
        self.dragon_card_fronts = [[], []]
        self.dragon_card_back = None
        self.tile_images = [[], []]
        self.player_card_images = [[], []]
        self.WIDTH, self.HEIGHT = 1400, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Fiery Dragon Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 54)
        self.state = 'HOMEPAGE'
        self.load_assets()
        self.homepage_frames = self.load_gif_frames('FieryDragonHomePageBg')
        self.frame_index = 0
        self.board = GameBoard(
            self.dragon_card_fronts, self.dragon_card_back, self.tile_images, self.player_card_images,
            (self.WIDTH, self.HEIGHT)
        )
        self.game_active = False
        self.popup_message = None
        self.popup_time = 0
        self.player_in_turn = 0
        self.number_of_player = 4
        self.still_your_turn = True
        self.flipped = False
        self.flipped_time = None
        self.flipped_card = None
        self.pos = [x.rect.center for x in self.board.tiles]
        self.token_pos = self.get_initial_pos()
        # cave position in the board relative to the board
        self.cave_pos = self.get_initial_pos()
        self.still_in_cave = [True, True, True, True]
        self.steps = [0, 0, 0, 0]

        self.homepage_play_button = Button(
            'START NEW GAME', self.WIDTH // 2 - 100, self.HEIGHT // 2 - 25, 395, 60,
            self.font, (0, 200, 0), self.start_game
        )
        self.homepage_score_board_button = Button(
            'SCORE BOARD', self.WIDTH // 2 - 100, self.HEIGHT // 2 + 50, 395, 60,
            self.font, (0, 0, 139), self.start_game
        )
        self.select_token_button = Button(
            'SELECT TOKEN', self.WIDTH // 2 - 100, self.HEIGHT // 2 - 175, 395, 60,
            self.font, (100, 100, 255), self.show_select_token_menu
        )
        self.start_button = Button(
            'Resume', 40, 640, 200, 50, self.font, (0, 255, 0), self.start_game
        )
        self.exit_button = Button(
            'Pause', 40, 700, 200, 50, self.font, (255, 0, 0), self.stop_game
        )
        self.shuffle_button = Button(
            'Shuffle', 40, 580, 200, 50, self.font, (100, 100, 255), self.shuffle_cards
        )
        self.return_home_button = Button(
            'Home', 40, 60, 200, 50, self.font, (255, 128, 128), self.return_home
        )
        self.save_button = Button(
            'Save', 40, 520, 200, 50, self.font, (0, 0, 255), self.show_save_game_menu
        )
        self.load_button = Button(
            'LOAD SAVED GAME', self.WIDTH // 2 - 100, self.HEIGHT // 2 - 100, 395, 60,
            self.font, (255, 128, 128), self.show_load_game_menu
        )
        self.back_button = Button(
            'BACK', 40, 700, 200, 50, self.font, (100, 100, 255), self.return_home
        )
        self.save_file_name = ""
        self.text_input_active = False
        self.current_player_selecting = 0
        self.selected_tokens = [None] * self.number_of_player
        self.available_tokens = [
            (128, 0, 128), (255, 255, 0), (173, 216, 230), (255, 192, 203)
        ]
        play_background_music("gameMusic.mp3")

    def load_gif_frames(self, path):
        """ Load and resize frames from the folder to uniform dimensions. """
        frames = []
        target_size = (self.WIDTH, self.HEIGHT)  # Set the target size to your desired dimensions
        for i in range(1, 9):
            frame_path = os.path.join(path, f'FieryDragonHomePageBg0{i}.png')
            try:
                image = pygame.image.load(frame_path)
                image = pygame.transform.scale(image, target_size)  # Resize the image
                frames.append(image)
            except Exception as e:
                print(f"Failed to load {frame_path}: {str(e)}")
        return frames

    def show_save_game_menu(self):
        self.state = 'SAVE_MENU'
        self.save_file_name = ""
        self.text_input_active = True

    def save_game(self):
        if self.save_file_name:
            filename = f"{self.save_file_name}.json"
            self.state_manager.save_game(filename)
            self.show_popup(f"Game saved as {filename}.", 2000)
            self.state = 'GAME'
            self.text_input_active = False

    def show_load_game_menu(self):
        self.state = 'LOAD_MENU'
        self.save_files = GameStateManager.list_save_files()

    def load_game(self, filename):
        self.state_manager.load_game(filename)
        self.show_popup(f"Game loaded from {filename}.", 2000)
        self.state = 'GAME'

    def delete_game(self, filename):
        os.remove(filename)
        self.save_files = GameStateManager.list_save_files()
        self.show_popup(f"Deleted {filename}.", 2000)

    def save_game_callback(self):
        self.show_save_game_menu()

    def load_game_callback(self):
        self.show_load_game_menu()

    def show_select_token_menu(self):
        print("Select Token Menu Opened")
        self.state = 'SELECT_TOKEN_MENU'
        self.current_player_selecting = 0  # Start with the first player
        self.selected_tokens = [None] * self.number_of_player
        self.available_tokens = [
            (128, 0, 128), (255, 255, 0), (173, 216, 230), (255, 192, 203)
        ]

    def handle_load_menu_click(self, pos):
        for index, filename in enumerate(self.save_files):
            y_pos = 100 + index * 60
            text_surface = self.font.render(filename, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(100, y_pos))
            delete_button_rect = pygame.Rect(500, y_pos, 80, 50)
            if text_rect.collidepoint(pos):
                self.load_game(filename)
                break
            elif delete_button_rect.collidepoint(pos):
                self.delete_game(filename)
                break

    def handle_save_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.save_game()
            elif event.key == pygame.K_BACKSPACE:
                self.save_file_name = self.save_file_name[:-1]
            else:
                self.save_file_name += event.unicode

    def handle_select_token_click(self, pos):
        print(f"Handling token selection click at position: {pos}")
        if self.current_player_selecting >= self.number_of_player:
            print("All players have selected their tokens. Returning to homepage.")
            self.state = 'HOMEPAGE'
            self.board.update_tokens(self.selected_tokens)
            return

        for index, color in enumerate(self.available_tokens):
            y_pos = 100 + index * 60
            token_rect = pygame.Rect(100, y_pos, 50, 50)
            print(f"Checking token at {token_rect} with color {color}")
            if token_rect.collidepoint(pos):
                print(f"Token selected: {color} for player {self.current_player_selecting + 1}")
                self.selected_tokens[self.current_player_selecting] = color
                self.current_player_selecting += 1
                self.available_tokens.pop(index)
                break

        print(f"Current player selecting: {self.current_player_selecting}")
        print(f"Selected tokens: {self.selected_tokens}")
        print(f"Available tokens: {self.available_tokens}")

    def load_assets(self):
        # Load the back of the card
        self.dragon_card_back = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "cardBack.png")),
            (self.card_width, self.card_height),
        )

        # List of card front names
        card_front_names = [
            "oneBat",
            "oneSpider",
            "oneBabyDragon",
            "oneSalamander",
            "twoBat",
            "twoSpider",
            "twoBabyDragon",
            "twoSalamander",
            "onePirateDragon",
            "twoPirateDragon",
            "threePirateDragon",
            "threeSalamander",
            "threeSpider",
            "threeBabyDragon",
            "threeBat",
            "PullBackToCave"
        ]

        # Load each card front image
        for name in card_front_names:
            image_path = os.path.join("assets", f"{name}.png")
            card_image = pygame.image.load(image_path)
            card_image = pygame.transform.scale(card_image, (self.card_width, self.card_height))
            self.dragon_card_fronts[0].append(card_image)
            self.dragon_card_fronts[1].append(name)

        # Load tile images
        tile_front_names = [
            "babyDragonVolcanoCard",
            "batVolcanoCard",
            "salamanderVolcanoCard",
            "spiderVolcanoCard",
        ]
        for name in tile_front_names:
            image_path = os.path.join("volcanocards", f"{name}.png")
            tile_image = pygame.image.load(image_path)
            tile_image = pygame.transform.scale(tile_image, (80, 100))
            self.tile_images[0].append(tile_image)
            self.tile_images[1].append(name)

            # Load player card images
            player_card_front_names = [
                "babyDragonInCave",
                "batInCave",
                "salamanderInCave",
                "spiderInCave",
            ]
            # Load each player card front image
            for name in player_card_front_names:
                image_path = os.path.join("playerCard", f"{name}.png")
                player_card_image = pygame.image.load(image_path)
                player_card_image = pygame.transform.scale(player_card_image, (90, 110))
                self.player_card_images[0].append(player_card_image)
                self.player_card_images[1].append(name)

    def next_player(self):
        if self.player_in_turn == self.number_of_player - 1:
            self.player_in_turn = 0
        else:
            self.player_in_turn += 1
        self.still_your_turn = True
        message = f"Now is Player {self.player_in_turn + 1}'s turn"
        self.show_popup(message, 2000)
        pygame.display.update()

    def get_initial_pos(self):
        token = self.board.tokens
        tile = self.board.tiles
        # ['Dragon', 'Bat', 'Salamander', 'Spider']
        hard_index = [(926, 626), (474, 626), (474, 174), (926, 174)]
        result = []
        for i in range(len(token)):
            for j in range(len(tile)):
                if hard_index[i] == tile[j].rect.center:
                    result.append(j)
                    break
        return result

    def move(self, card, player_index):
        # movement function
        players = self.board.tokens
        player = players[player_index]
        new_pos_index = self.token_pos[player_index]
        steps = 0
        if player.currently_on.animal != card.animal:
            if card.animal == "Pirate" and not player.still_in_cave:
                steps = -card.number
                new_pos_index = new_pos_index - card.number
                if new_pos_index < - len(self.pos):
                    new_pos_index = new_pos_index + len(self.pos)
            elif card.animal == "PullBackToCave":
                if player.still_in_cave:
                    return
                else:
                    position = self.token_pos[self.player_in_turn]
                    start = None
                    if position < 0:
                        position = position + len(self.pos)
                    # get the nearest backward cave index
                    for i in range(len(self.cave_pos) - 1):
                        if self.cave_pos[i] <= position < self.cave_pos[i + 1]:
                            start = i
                            break
                    # indexing issue when player is at behind the first cave
                    # in the array which the last cave in the array first cave
                    # behind the player
                    if start == None:
                        start = len(self.cave_pos) - 1
                    # while loop to go backwards to find the first empty cave
                    index = start
                    found = False
                    while not found:
                        if self.board.player_cards[index].empty:
                            player.currently_on = self.board.player_cards[index]
                            player.still_in_cave = True
                            self.board.player_cards[index].empty = False
                            found = True
                            break
                        index -= 1
                    steps = -(position - self.cave_pos[index])
                    if position < self.cave_pos[start]:
                        steps = -(position + (len(self.board.tiles) - self.cave_pos[index]) + 1)
                    self.steps[player_index] += steps
                    self.token_pos[player_index] = self.cave_pos[index]
                    return
            # when card animal not equal tile or pirate card still in cave
            else:
                self.still_your_turn = False
                return None
        # if dragon card can make player move forward
        else:
            steps = card.number
            new_pos_index = new_pos_index + card.number
            # went out of cave move like one tile backwards from the closest tile near the cave
            if player.still_in_cave:
                new_pos_index -= 1
            if len(self.pos) - 1 < new_pos_index:
                new_pos_index = new_pos_index - len(self.pos)
            # only way to move out of the cave
            if player.still_in_cave:
                player.still_in_cave = False
                player.currently_on.empty = True
        # if player's target tile already have a player, don't move
        for i in range(len(self.token_pos)):
            if new_pos_index == self.token_pos[i] and not players[i].still_in_cave:
                self.still_your_turn = False
                return None
        self.steps[player_index] += steps
        self.token_pos[player_index] = new_pos_index
        player.currently_on = self.board.tiles[new_pos_index]
        return

    def check_win(self):
        current_player_step = self.steps[self.player_in_turn]
        if current_player_step > 0 and current_player_step % 24 == 0:
            self.game_active = False
            t = self.board.tokens[self.player_in_turn]
            t.currently_on = t.player_c
            message = f"Player {self.player_in_turn + 1} Wins!!!!"
            saveScore(self.player_in_turn + 1)
            self.show_popup(message, 2000)
            pygame.display.update()

    def start_game(self):
        self.game_active = True
        self.state = 'GAME'
        self.reset_game_record()
        message = f"Game Start!!!!{self.board.tokens[self.player_in_turn].player_c.animal} First"
        self.show_popup(message, 2000)
        pygame.display.update()

    def reset_game_record(self):
        # Reload the initial variable
        self.game_active = True
        self.popup_message = None
        self.popup_time = 0
        # Record the player in the turn
        self.player_in_turn = 0
        self.number_of_player = 4
        self.still_your_turn = True
        # card flip back after 2 seconds,other part under, variable stored
        self.flipped = False
        self.flipped_time = None
        self.flipped_card = None
        # board tile position
        self.pos = [x.rect.center for x in self.board.tiles]
        # board position of token
        self.token_pos = self.get_initial_pos()
        # cave position in the board relative to the board
        self.cave_pos = self.get_initial_pos()
        # calculate steps to win
        self.steps = [0, 0, 0, 0]
        for i in self.board.tokens:
            i.currently_on = i.player_c
            i.still_in_cave = True

    def shuffle_cards(self):
        if self.game_active:
            self.board.shuffle_dragon_cards()
            self.board.draw(self.screen)
            self.show_popup("The chits have been shuffled", 2000)
            self.still_your_turn = True
            pygame.display.update()

    def stop_game(self):
        self.game_active = False
        self.show_popup("Your turn has ended, please wait for the next round.", 2000)
        for card in self.board.cards:
            if card.is_flipped:
                card.flip()
        self.board.draw(self.screen)
        pygame.display.flip()

    def return_home(self):
        self.state = 'HOMEPAGE'

    def show_popup(self, message, duration):
        self.popup_message = message
        self.popup_time = pygame.time.get_ticks() + duration

    def run(self):
        running = True
        frame_change_tick = 0  # To control the speed of animation
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'HOMEPAGE':
                        if self.homepage_play_button.rect.collidepoint(event.pos):
                            self.start_game()
                        if self.homepage_score_board_button.rect.collidepoint(event.pos):
                            print("scoreboard")
                            from ScoreBoard import ScoreBoard
                            ScoreBoard().active(self.screen)
                        if self.load_button.rect.collidepoint(event.pos):
                            self.load_button.handle_event(event)
                        if self.select_token_button.rect.collidepoint(event.pos):
                            self.select_token_button.handle_event(event)
                    elif self.state == 'GAME':
                        if self.save_button.rect.collidepoint(event.pos):
                            self.save_button.handle_event(event)
                        if self.start_button.rect.collidepoint(event.pos):
                            self.start_button.handle_event(event)
                        elif self.exit_button.rect.collidepoint(event.pos):
                            self.exit_button.handle_event(event)
                        elif self.shuffle_button.rect.collidepoint(event.pos):
                            self.shuffle_button.handle_event(event)
                        elif self.return_home_button.rect.collidepoint(event.pos):
                            self.return_home_button.handle_event(event)
                        else:
                            if self.game_active:
                                for card in self.board.cards:
                                    if card.rect.collidepoint(event.pos) and not self.flipped:
                                        card.flip()
                                        self.move(card, self.player_in_turn)
                                        self.check_win()
                                        self.flipped_time = pygame.time.get_ticks()
                                        self.flipped = True
                                        self.flipped_card = card
                                        if not self.still_your_turn:
                                            self.next_player()
                    elif self.state == 'LOAD_MENU':
                        self.handle_load_menu_click(event.pos)
                        if self.back_button.rect.collidepoint(event.pos):
                            self.back_button.handle_event(event)
                    elif self.state == 'SELECT_TOKEN_MENU':
                        self.handle_select_token_click(event.pos)
                        if self.back_button.rect.collidepoint(event.pos):
                            self.back_button.handle_event(event)
                elif event.type == pygame.KEYDOWN:
                    if self.state == 'SAVE_MENU':
                        self.handle_save_menu_events(event)

            self.screen.fill((0, 0, 0))
            if self.state == 'HOMEPAGE':
                # Update the frame index and draw the frame for the homepage animation
                if pygame.time.get_ticks() - frame_change_tick > 300:  # Adjust the timing for slower animation
                    self.frame_index = (self.frame_index + 1) % len(self.homepage_frames)
                    frame_change_tick = pygame.time.get_ticks()

                self.screen.blit(self.homepage_frames[self.frame_index], (0, 0))
                self.homepage_play_button.draw(self.screen)
                self.load_button.draw(self.screen)
                self.select_token_button.draw(self.screen)
                self.homepage_score_board_button.draw(self.screen)
            elif self.state == 'GAME':
                self.save_button.draw(self.screen)
                self.start_button.draw(self.screen)
                self.exit_button.draw(self.screen)
                self.shuffle_button.draw(self.screen)
                self.return_home_button.draw(self.screen)
                self.board.draw(self.screen)
                if self.flipped:
                    if pygame.time.get_ticks() - self.flipped_time > 1000:
                        self.flipped = False
                        self.flipped_card.flip()
            elif self.state == 'LOAD_MENU':
                self.back_button.draw(self.screen)
                for index, filename in enumerate(self.save_files):
                    y_pos = 100 + index * 60
                    text_surface = self.font.render(filename, True, (255, 255, 255))
                    self.screen.blit(text_surface, (100, y_pos))
                    delete_surface = self.font.render("Delete", True, (255, 0, 0))
                    self.screen.blit(delete_surface, (500, y_pos))
            elif self.state == 'SAVE_MENU':
                prompt_surface = self.font.render("Enter File Name:", True, (255, 255, 255))
                self.screen.blit(prompt_surface, (100, 100))
                filename_surface = self.font.render(self.save_file_name, True, (255, 255, 255))
                self.screen.blit(filename_surface, (100, 200))
            elif self.state == 'SELECT_TOKEN_MENU':
                prompt_surface = self.font.render(f"Player {self.current_player_selecting + 1} Select Token:", True,
                                                  (255, 255, 255))
                self.screen.blit(prompt_surface, (500, 100))
                for index, color in enumerate(self.available_tokens):
                    y_pos = 100 + index * 60
                    pygame.draw.rect(self.screen, color, (100, y_pos, 50, 50))
                self.back_button.draw(self.screen)

            title_surface = self.font.render('Fiery Dragon', True, (255, 255, 255))
            self.screen.blit(title_surface, (10, 10))

            if self.popup_message and pygame.time.get_ticks() < self.popup_time:
                popup_surface = self.font.render(self.popup_message, True, (255, 255, 255))
                popup_rect = popup_surface.get_rect(center=(self.WIDTH // 2, 100))
                background_surface = pygame.Surface((popup_rect.width + 20, popup_rect.height + 20), pygame.SRCALPHA)
                background_surface.fill((50, 50, 50, 200))
                background_rect = background_surface.get_rect(center=(self.WIDTH // 2, 100))
                self.screen.blit(background_surface, background_rect)
                self.screen.blit(popup_surface, popup_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
