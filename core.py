import pygame


class Car:
    def __init__(self, surface, position, speed):
        self.original_surface = surface
        self.surface = self.original_surface
        self.x, self.y = position
        self.angle = 0
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = speed

    def rotate(self, angle):
        self.angle = self.angle + angle
        self.surface = pygame.transform.rotate(self.original_surface, -self.angle)
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def move(self):
        self.x = self.x + self.direction.x * self.speed
        self.y = self.y + self.direction.y * self.speed


def main():
    pygame.init()
    pygame.display.set_caption('minimal program')

    car_surface = pygame.image.load('data/car.png')
    car = Car(car_surface, (0,300), 10)

    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    car.draw(screen)

    running = True
    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pygame.display.update()


if __name__ == "__main__":
    main()
