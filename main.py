import pygame
from game.game_engine import GameEngine

def main():
    pygame.init()
    pygame.mixer.init()  # initialize sound

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ping Pong Game")

    clock = pygame.time.Clock()
    engine = GameEngine(width, height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()

        screen.fill((0, 0, 0))
        engine.render(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
