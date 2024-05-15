import pygame
from View.Button import Button
class LeaderBoardView():
    def __init__(self, screen, leaderboard):
        self.leaderboard = leaderboard
        self.page = 1
        self.records_per_page = 10
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        pygame.display.set_caption('Leaderboard')
        self.clock = pygame.time.Clock()
        self.run = True


        button_width, button_height = 100, 50
        self.button_left = Button(self.screen,(50, 350), button_width, button_height, "Prev", self.prev_page)
        self.button_right = Button(self.screen,(250, 350), button_width, button_height, "Next", self.next_page)

    def update(self):
        self.screen.fill((255, 255, 255))
        self.button_left.update()
        self.button_right.update()
        start_index = (self.page - 1) * self.records_per_page
        end_index = start_index + self.records_per_page
        page_records = self.leaderboard.get_leaderboard()[start_index:end_index]

        for i, (name, score) in enumerate(page_records):
            text_surface = self.font.render(f"{name}: {score}", True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 50 + i * 30))

    def handle_event(self, event):
        self.button_left.handle_event(event)
        self.button_right.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.run = False
                pygame.time.wait(300)
                return

    def prev_page(self):
        self.page = max(1, self.page - 1)
        pygame.time.wait(300)

    def next_page(self):
        max_pages = len(self.leaderboard.get_leaderboard()) // self.records_per_page
        self.page = min(max_pages, self.page + 1)
        pygame.time.wait(300)


