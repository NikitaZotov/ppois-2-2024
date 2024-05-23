from collision_detection import *
from core.game_modifiers import Modifiers
from core.game_status import GameStatus
from game_screens import *
from level import LevelHandler
from paddle import Paddle

class GameManager:
    def __init__(self, records_manager):
        self.records_manager = records_manager

    def run_game(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        all_sprites = pygame.sprite.Group()
        clock = pygame.time.Clock()

        level = show_select_level()

        bricks, walls = LevelHandler.create_level(level)
        all_sprites.add(bricks)
        all_sprites.add(walls)
        paddle = Paddle()
        ball = Ball()
        all_sprites.add(paddle)
        all_sprites.add(ball)

        balls = [ball]

        collision = Collision()
        start_time = time.time()
        level_completed = False

        GameStatus.set_run()
        while GameStatus.run_status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        paddle.speed = -PADDLE_SPEED
                    elif event.key == pygame.K_RIGHT:
                        paddle.speed = PADDLE_SPEED
                    elif event.key == pygame.K_ESCAPE:
                        GameStatus.set_pause()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and paddle.speed < 0:
                        paddle.speed = 0
                    elif event.key == pygame.K_RIGHT and paddle.speed > 0:
                        paddle.speed = 0

            collision.check_collision(balls, bricks, walls, paddle, all_sprites)

            Modifiers.add_game_modifier(balls, paddle, all_sprites, collision)

            if len(bricks) == 0:
                level_completed = True

            if len(balls) == 0 or not GameStatus.run_status:
                GameStatus.set_pause()
                MusicHandler.play_sad_music()
                show_game_over_text()
                return

            all_sprites.update()

            screen.fill(BLACK)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(60)

            if level_completed:
                end_time = time.time()
                level_time = (end_time - start_time).__round__(3)
                start_time = end_time

                if LevelHandler.current_level_index in self.records_manager.records:
                    previous_record_time = self.records_manager.records[LevelHandler.current_level_index]['time']
                    if level_time < previous_record_time:
                        show_save_record_screen(level=LevelHandler.current_level_index, time=level_time)
                else:
                    self.records_manager.add_record(LevelHandler.current_level_index, "Player", level_time)
                show_level_completed_screen(level=LevelHandler.current_level_index, time=level_time)
                return

if __name__ == "__main__":
    pygame.init()
    records_manager = RecordsManager()
    game_manager = GameManager(records_manager)

    while True:
        choice = show_menu()
        if choice == 0:
            game_manager.run_game()
        elif choice == 1:
            show_records_screen(records_manager)
        elif choice == 2:
            show_help_screen()
            pass
        elif choice == 3:
            pygame.quit()
            sys.exit()
