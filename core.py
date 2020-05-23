import pygame
import runpy

FPS = 30


class Car(pygame.sprite.Sprite):
    def __init__(self, surface, position, speed, actions, *groups):
        super(Car, self).__init__(*groups)
        self.orig_image = surface
        self.image = self.orig_image
        self.x, self.y = position
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.angle = 0
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 0
        self.max_speed = speed
        self.actions = actions

    def rotate(self, angle):
        self.angle = self.angle + angle
        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x = self.x + self.direction.x * self.speed
        self.y = self.y + self.direction.y * self.speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def _start(self):
        self.speed = self.max_speed

    def _stop(self):
        self.speed = 0

    def go(self):
        self.actions.extend([lambda: self._start(), lambda: self._stop()])

    def left(self):
        self.actions.append(lambda: self.rotate(-90))

    def right(self):
        self.actions.append(lambda: self.rotate(-90))


def event_generator(car):
    car.go()
    car.left()
    car.go()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Learn Python')

    action_list = []

    sprites = pygame.sprite.Group()
    car = Car(pygame.image.load('data/car.png'), (16, 300), 64/FPS, action_list, sprites)
    car.rotate(90)

    runpy.run_module('executor', {'car': car})
    # simport executor
    #event_generator(car)

    actions = iter(action_list)

    screen = pygame.display.set_mode((800, 600))

    running = True
    elapsed = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

        elapsed = elapsed + clock.get_time()
        if elapsed > 1000:
            elapsed = 0
            action = next(actions, None)
            if action:
                action()

        sprites.update()
        screen.fill((255, 255, 255))
        sprites.draw(screen)
        clock.tick(30)


if __name__ == "__main__":
    main()
