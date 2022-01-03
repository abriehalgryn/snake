import time
import pygame
import random

# things to do
# when all the spaces are full, the came will freeze (while loop not ending)
# update the snake head and tale instead of every cell
# make it smooth
# resizing
# textures
# snake length counter - done
# snake can eat itself if moving left then right is pressed - done kinda buggy (overrites if you  press up then left quicklu) - done

DEBUG = False

EMPTY = 0
SNAKE = 1
FOOD = 2

WHITE = (255, 255, 255)

COLORS = [
    (0, 0, 0),
    (70, 220, 70),
    (220, 70, 70)
]

class SnakeGame:
    def __init__(self,
                 width=25, height=25,
                 screen_width=500, screen_height=500):

        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.square_width = 0
        self.square_height = 0
        self.calculate_square_size()

        # initial snake position (starting pos) 
        self.snake_xpos = self.width // 2
        self.snake_ypos = self.height // 2

        self.x_change_list = [1]
        self.y_change_list = [0]

        self.snake_speed = 0.1
        self.growth_rate = 2

        self.food_xpos = 0
        self.food_ypos = 0

        self.start_size = 3
        self.snake_length = self.start_size
        self.snake_body = []

        self.board = None
        self.create_board()
        self.draw_snake()

        self.alive = True

    def initiate_pygame(self):
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("SNAKEY")
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.RESIZABLE
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.alive = False
                break

            elif event.type == pygame.KEYDOWN:
                if DEBUG: print(event.key)
                if event.key == pygame.K_SPACE:
                    if DEBUG: print("space")

                if event.key == pygame.K_LEFT:
                    if self.x_change_list[-1] != 1:
                        if DEBUG: print("Left key pressed")
                        self.x_change_list.append(-1)
                        self.y_change_list.append(0)
                elif event.key == pygame.K_RIGHT:
                    if self.x_change_list[-1] != -1:
                        if DEBUG: print("Right key pressed")
                        self.x_change_list.append(1)
                        self.y_change_list.append(0)
                elif event.key == pygame.K_UP:
                    if self.y_change_list[-1] != 1:
                        if DEBUG: print("Up key pressed")
                        self.x_change_list.append(0)
                        self.y_change_list.append(-1)
                elif event.key == pygame.K_DOWN:
                    if self.y_change_list[-1] != -1:
                        if DEBUG: print("Down key pressed")
                        self.x_change_list.append(0)
                        self.y_change_list.append(1)


            elif event.type == pygame.VIDEORESIZE:
                if DEBUG: print(event.w, event.h)

    def mainloop(self):
        self.spawn_food()
        start_time = time.time() 

        while self.alive:
            self.handle_events()

            time_passed = time.time() - start_time

            if time_passed > self.snake_speed:
                if self.snake_crash():
                    self.alive = False
                    break

                self.snake_xpos += self.x_change_list[0]
                self.snake_ypos += self.y_change_list[0]

                if len(self.x_change_list) >1 and len(self.y_change_list) >1:
                    self.x_change_list.pop(0)
                    self.y_change_list.pop(0)

                self.draw_snake()
                self.draw_board()
                self.display_score()



                start_time = time.time() 
                pygame.display.flip()

            self.clock.tick(60)

        print("You Died")
        print("Score: " + str(self.snake_length - self.start_size))

    def calculate_square_size(self):
        self.square_width = self.screen_width / self.width
        self.square_height = self.screen_height / self.height

    def create_board(self):
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width): 
                row.append(EMPTY)
            self.board.append(row)

    def print_board(self):
        for i, row in enumerate(self.board):
            if DEBUG: print(i, row)

    def randomize_board(self):
        for row in self.board:
            for i in range(len(row)):
                row[i] = random.randint(0, 2)

    def draw_square(self, x, y, square_type):
        pygame.draw.rect(
            self.screen, 
            COLORS[square_type],
            (
                int(self.square_width * x),
                int(self.square_height * y),
                int(self.square_width),
                int(self.square_height),
            )
        )

    def draw_board(self):
        for i, row in enumerate(self.board):
            for j, square_type in enumerate(row):
                self.draw_square(j, i, square_type)

    def draw_snake(self):

        if self.board[self.snake_ypos][self.snake_xpos] == FOOD:
            self.snake_length += self.growth_rate 
            self.spawn_food()

        self.board[self.snake_ypos][self.snake_xpos] = SNAKE

        self.snake_body.append((
            self.snake_ypos, self.snake_xpos
        ))

        if len(self.snake_body) > self.snake_length:
            self.board[self.snake_body[0][0]][self.snake_body[0][1]] = EMPTY
            self.snake_body.pop(0)

        if DEBUG: print("Body list:", self.snake_body)
        if DEBUG: print("Length of Snake:", len(self.snake_body))
        self.print_board()

    def spawn_food(self):
        self.food_xpos = random.randint(0, self.width-1)
        self.food_ypos = random.randint(0, self.height-1)

        while True:
            if self.board[self.food_ypos][self.food_xpos] == EMPTY:
                self.board[self.food_ypos][self.food_xpos] = FOOD
                break
            else:
                self.food_xpos = random.randint(0, self.width-1)
                self.food_ypos = random.randint(0, self.height-1)


    def snake_crash(self):
        # if the snake hits a border
        if self.snake_xpos + self.x_change_list[0] < 0 \
                or self.snake_xpos + self.x_change_list[0] > self.width - 1 \
                or self.snake_ypos + self.y_change_list[0]< 0 \
                or self.snake_ypos + self.y_change_list[0] > self.height - 1:\
            return True

        # if the snake eats itself
        elif self.board[self.snake_ypos + self.y_change_list[0]][self.snake_xpos + self.x_change_list[0]] == SNAKE:
            return True

    def display_score(self):
        score = "Score: " + str(self.snake_length - self.start_size)
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(score, False, WHITE)
        self.screen.blit(textsurface,(0,0))
    

while True: 
    snake = SnakeGame()
    # snake.randomize_board()      # dont want to do this atm  cause just testing around with the actual snake movement
    snake.initiate_pygame()
    snake.mainloop()

