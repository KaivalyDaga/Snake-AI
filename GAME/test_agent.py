import Environment as Env
import pygame
import random
from pygame.math import Vector2
import numpy as np
import copy
import math
import os
import sys
import matplotlib.pyplot as plt
# from statistics import mean
# from itertools import chain


class Agent:
    def __init__(self):
        self.env = Env.Game()
        # Game environment
        self.actions = [0, 1, 2, 3]
        # 0-3 is N, W, S, E
        self.state = self.state_locator()
        self.obs = self.obs_locator()
        self.qmatrix = np.zeros((8, 15, 4), dtype=int)
        self.qmatrix_old = np.zeros((8, 15, 4), dtype=int)
        self.qmatrix_new = np.zeros((8, 15, 4), dtype=int)

    def obs_locator(self):
        up = left = down = right = 0
        x0 = self.env.snake.body[0].x
        y0 = self.env.snake.body[0].y
        v0 = Vector2(x0, y0 - 1)
        v1 = Vector2(x0 - 1, y0)
        v2 = Vector2(x0, y0 + 1)
        v3 = Vector2(x0 + 1, y0)
        x1 = self.env.snake.body[0].x == 0
        y1 = self.env.snake.body[0].y == 0
        x2 = self.env.snake.body[0].x == 19
        y2 = self.env.snake.body[0].y == 19
        if v0 in self.env.snake.body[:] or y1:
            up = 1
        if v1 in self.env.snake.body[:] or x1:
            left = 1
        if v2 in self.env.snake.body[:] or y2:
            down = 1
        if v3 in self.env.snake.body[:] or x2:
            right = 1
        return 8*up + 4*left + 2*down + right - 1

    def state_locator(self):
        """
        current: 0-7 are respectively NE, NW, SW, SE, E, N, W, S
        :return: respective current state
        """
        x1 = self.env.fruit.x > self.env.snake.body[0].x
        y1 = self.env.fruit.y > self.env.snake.body[0].y
        x2 = self.env.fruit.x < self.env.snake.body[0].x
        y2 = self.env.fruit.y < self.env.snake.body[0].y
        if x1:
            if y2:
                return 0
            elif y1:
                return 3
            else:
                return 4
        elif x2:
            if y2:
                return 1
            elif y1:
                return 2
            else:
                return 6
        elif y1:
            return 7
        else:
            return 5

    def greedy_action(self):
        action_val = self.qmatrix[self.state][self.obs]
        return np.argmax(action_val)

    def state_value(self):
        values = self.qmatrix[self.state]
        # return (1 - epsilon) * np.max(values) + epsilon * np.sum(values)
        return np.max(values)

    @staticmethod
    def exploration(current, action):
        reward = 1
        if current == 0:
            if action == 0 or action == 3:
                return reward
        elif current == 1:
            if action == 0 or action == 1:
                return reward
        elif current == 2:
            if action == 1 or action == 2:
                return reward
        elif current == 3:
            if action == 2 or action == 3:
                return reward
        elif current == 5:
            if action == 0:
                return reward
        elif current == 6:
            if action == 1:
                return reward
        elif current == 7:
            if action == 2:
                return reward
        elif current == 4:
            if action == 3:
                return reward
        return -2*reward

    def take_action(self, check, _fruit, num):
        epsilon = 0.1/math.sqrt(num)
        gamma = 0.5
        while True:
            if random.random() < epsilon:
                action = random.choice(self.actions)
            #    print("Random")
            else:
                action = self.greedy_action()
            #    print("Greedy")

            if action == 0:  # and not self.env.snake.direction == Vector2(0, 1):
                self.env.snake.direction = Vector2(0, -1)
                break
            elif action == 1:  # and not self.env.snake.direction == Vector2(1, 0):
                self.env.snake.direction = Vector2(-1, 0)
                break
            elif action == 2:  # and not self.env.snake.direction == Vector2(0, -1):
                self.env.snake.direction = Vector2(0, 1)
                break
            elif action == 3:  # and not self.env.snake.direction == Vector2(-1, 0):
                self.env.snake.direction = Vector2(1, 0)
                break

        current = copy.deepcopy(self.state)
        current_obstacle = copy.deepcopy(self.obs)

        self.env.snake.move_snake()

        reward = 0
        if self.env.check_fail():
            reward += -300
            # episode ends after it dies
            check = False
        if self.env.check_collision():
            reward += 30
            _fruit[num - 1] += 1

        if num % 50 == 1 and int(num/50) % 2 == 0:
            self.qmatrix_old = copy.deepcopy(self.qmatrix)
        reward += self.exploration(current, action)
        self.state = self.state_locator()
        self.obs = self.obs_locator()
        self.qmatrix[current][current_obstacle][action] += \
            gamma * (reward + 0.5*self.state_value() - self.qmatrix[current][current_obstacle][action])
        if num % 50 == 1 and int(num/50) % 2 == 1:
            self.qmatrix_new = copy.deepcopy(self.qmatrix)

        return check

    def plot_graphs(self, __fruit):
        # stores average of every 10 episodes
        splitsize = 10
        __fruit = [sum(__fruit[i:i+splitsize])//splitsize for i in range(0, len(__fruit), splitsize)]
        del __fruit[-1]
        # arange gives uniform array
        episodes = np.arange(1, len(__fruit)+1)
        plt.plot(episodes, __fruit)
        plt.xlabel("Per 10 Episodes")
        plt.ylabel("Average Fruits")
        plt.savefig("fruits_episodes_1.png")
        plt.close()
        return

    def episode(self, __fruit,  num):
        check = True
        while check:
            check = agent.take_action(check, __fruit, num)
            screen.fill((175, 215, 70))
            agent.env.draw_elements()
            pygame.display.update()
            clock.tick(100000)
        if (num > 1 and np.allclose(self.qmatrix_new, self.qmatrix_old, 0, 0.01)) or num > 600:
            np.save("qmatrix_5", self.qmatrix)
            self.plot_graphs(__fruit)
            sys.exit()
        print(num)


os.getcwd()
dirname = os.path.dirname(__file__)
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("Snake Game-Training")
clock = pygame.time.Clock()
filename = os.path.join(dirname, 'Graphics/apple.png')
apple = pygame.image.load(filename).convert_alpha()
game_font = pygame.font.SysFont('comicsansms', 25)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

agent = Agent()
n = 0
fruit = []

while True:
    n += 1
    fruit.append(0)
    agent.episode(fruit, n)
