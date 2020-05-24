import time
import pygame
import asyncio
import executor

FPS = 30


class Car(pygame.sprite.Sprite):
    def __init__(self, surface, position, screen, *groups):
        super(Car, self).__init__(*groups)
        self.screen = screen
        self.orig_image = surface
        self.image = self.orig_image
        self.rect = self.image.get_rect(center=position)
        self.angle = 0
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 0
        self.cell_width = max(self.rect.width, self.rect.height)

    def rotate(self, angle):
        self.angle = self.angle + angle
        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)

    def _next_move(self, speed):
        move = self.rect.move((self.direction.x * speed, self.direction.y * speed))
        return move

    def update(self):
        move = self._next_move(self.speed)
        if self.is_legal_move(move):
            self.rect = move

    def is_legal_move(self, move):
        screen = self.screen.get_rect()
        new_screen = move.union(screen)
        return new_screen == screen

    def at_border(self):
        move = self._next_move(self.cell_width / FPS)
        return not self.is_legal_move(move)

    def go(self):
        self.speed = self.cell_width/FPS
        time.sleep(1/FPS)
        self.speed = 0

    def turn(self, angle):
        frames = int(FPS*(abs(angle)/90.))
        frames = frames or 1
        delta = angle/frames
        for i in range(frames):
            self.rotate(delta)
            time.sleep(1/FPS)

    def left(self):
        self.rotate(-90)
        #self.turn(-90)

    def right(self):
        #self.turn(90)
        self.rotate(90)


async def pygame_loop(screen, sprites):
    running = True
    current_time = 0
    loop = asyncio.get_event_loop()
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            last_time, current_time = current_time, loop.time()
            await asyncio.sleep(1/FPS - (current_time-last_time))

            screen.fill((255, 255, 255))
            sprites.update()
            sprites.draw(screen)
            pygame.display.flip()
    finally:
        loop.stop()


def main():
    loop = asyncio.get_event_loop()

    pygame.init()
    pygame.display.set_caption('Learn Python')
    screen = pygame.display.set_mode((800, 600))

    sprites = pygame.sprite.Group()
    car = Car(pygame.image.load('data/car.png'), (33, 300), screen, sprites)
    car.rotate(90)

    asyncio.ensure_future(pygame_loop(screen, sprites))
    loop.run_in_executor(None, executor.task, car)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    pygame.quit()


if __name__ == "__main__":
    main()
