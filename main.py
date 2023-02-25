import pygame as pg
from random import randrange


pg.init()

WINDOW = 700
TILE_SIZE = 50

RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
segments = [snake.copy()]

snake_dir = (0, 0)  # default
time, time_step = 0, 100    # movement speed control

food = snake.copy()
food.center = get_random_position()

screen = pg.display.set_mode([WINDOW, WINDOW])
pg.display.set_caption("Not So Standard Snake - NSSS")
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}  # default

length = 1
score = 0
paused = False

background = pg.image.load('background_snake.jpg')
animation_images = [pg.image.load(f'frame{i}.png') for i in range(1, 8)]


# animation function
def play_animation():
    for img in animation_images:
        screen.blit(background, (0, 0))  # draw background between each frame
        [pg.draw.rect(screen, 'green', segment) for segment in segments]    # draw snake
        scaled_img = pg.transform.scale(img, (2 * TILE_SIZE, 2 * TILE_SIZE))    # animation scale
        screen.blit(scaled_img, (snake.centerx - TILE_SIZE, snake.centery - TILE_SIZE))  # animation location
        pg.display.flip()
        pg.time.delay(30)   # delay between frames


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            # up # dirs prevent from selfeating # last condition is preventing from moving out of visible space
            if event.key == pg.K_w and dirs[pg.K_w] and 0 < snake.centerx < WINDOW:
                snake_dir = (0, -TILE_SIZE)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s] and 0 < snake.centerx < WINDOW:
                snake_dir = (0, TILE_SIZE)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a] and 0 < snake.centery < WINDOW:
                snake_dir = (-TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d] and 0 < snake.centery < WINDOW:
                snake_dir = (TILE_SIZE, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_ESCAPE:
                exit()

    screen.blit(background, (0, 0))

    if not paused:
        # check selfeating
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if self_eating:
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]
            score = 0

        # check borders and teleport snake
        if snake.left < 0:
            snake.center = (WINDOW + TILE_SIZE / 2, snake.centery)

        elif snake.right > WINDOW:
            snake.center = (- TILE_SIZE / 2, snake.centery)

        elif snake.top < 0:
            snake.center = (snake.centerx, WINDOW + TILE_SIZE / 2)

        elif snake.bottom > WINDOW:
            snake.center = (snake.centerx, - TILE_SIZE / 2)

        # check food
        if snake.colliderect(food):
            play_animation()
            food.center = get_random_position()
            length += 1
            score += 1

        # draw food
        pg.draw.rect(screen, 'red', food)

        # draw snake
        [pg.draw.rect(screen, 'green', segment) for segment in segments]

        # move snake
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

        # draw score
        font = pg.font.Font("freesansbold.ttf", 20)
        score_display = font.render("Score: " + str(score), True, (255, 0, 0))
        screen.blit(score_display, (WINDOW - 125, 20))

        pg.display.flip()
        clock.tick(60)
