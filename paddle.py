import pygame

class Paddle:
    def __init__(self, x, y, width, height, speed, screen_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.screen_height = screen_height

    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

        # Keep paddle inside screen
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
