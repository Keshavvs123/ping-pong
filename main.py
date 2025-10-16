import pygame
from game.game_engine import GameEngine

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()  # for sound effects

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

def choose_match_target(screen, font):
    """Display replay options and wait for user input"""
    choosing = True
    match_target = 5  # default

    while choosing:
        screen.fill(BLACK)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, option in enumerate(options):
            text_surface = font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 60 + i*40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    match_target = 2  # Best of 3 → first to 2
                    choosing = False
                elif event.key == pygame.K_5:
                    match_target = 3  # Best of 5 → first to 3
                    choosing = False
                elif event.key == pygame.K_7:
                    match_target = 4  # Best of 7 → first to 4
                    choosing = False
                elif event.key == pygame.K_ESCAPE:
                    return None
    return match_target

def main():
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    # Default winning score
    winning_score = 5

    while running:
        SCREEN.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input(events)
        engine.update()
        engine.render(SCREEN)

        # Check if game is over
        if engine.check_game_over(SCREEN, winning_score):
            # Replay options
            match_target = choose_match_target(SCREEN, engine.font)
            if match_target is None:  # player chose ESC or closed window
                running = False
            else:
                winning_score = match_target
                engine.reset_game()  # reset scores and ball

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()


