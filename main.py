import pygame

if __name__ == '__main__':
    print('Welcome!')
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH_SCREEN = 300
    HEIGHT_SCREEN = 550
    BACKGROUND_COLOR = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            # here we are checking if the user wants to exit the game
            if event.type == pygame.QUIT:
                print('Mory is closing the game')
                exit(0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            print('Right was pressed')
        elif keys[pygame.K_LEFT]:
            print('Left was pressed')
        elif keys[pygame.K_UP]:
            print('Up was pressed')
        elif keys[pygame.K_DOWN]:
            print('Down was pressed')
        elif keys[pygame.K_ESCAPE]:
            print('Mory is closing the game, he has pressed Escape button')
            exit(0)

        # Very important each frame we should use to  put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate independent physics.
        dt = clock.tick(20) / 1000

    pygame.quit()
