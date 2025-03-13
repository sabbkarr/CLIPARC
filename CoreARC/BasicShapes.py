import numpy as np
import math
import matplotlib.pyplot as plt
from random import choice
import random

class BasicShapes:
    """
    def __init__(self, grid_size_x, grid_size_y):
        self.grid = np.zeros((grid_size_y, grid_size_x), dtype=int)

    def place_shape(self, shape_bitmap, x, y, colors):
        shape_h, shape_w = shape_bitmap.shape
        grid_h, grid_w = self.grid.shape
        if x + shape_h > grid_h or y + shape_w > grid_w:
            print("Shape placement out of bounds.")
            return
        if np.any(self.grid[x:x + shape_h, y:y + shape_w] != 0):
            print("Shape placement overlaps with existing grid elements.")
        self.grid[x:x + shape_h, y:y + shape_w] += self.apply_color(shape_bitmap, colors)

    def apply_color(self, mask, color):
        if isinstance(color, np.ndarray):
            return mask * self.motif(mask, color)
        elif color == "random":
            return mask * np.random.randint(1, 10, size=mask.shape)
        else:
            return mask * np.full(mask.shape, color)
    """
    # Basic Shapes
    def rectangle(self, length, height):
        if length == height:
            length = length + 1
        return np.ones((length + 1, height + 1), dtype=int)
    def square(self, length):
        return np.ones((length + 1, length + 1), dtype=int)
    def hline(self, length):
        return np.ones((length + 3, 1), dtype=int)
    def vline(self, length):
        return np.ones((1, length + 3), dtype=int)
    def plus(self, length, height, thickness):
        if length < height:
            height = min(length * 2, height)
        else:
            length = min(height * 2, length)
        thickness = min(min(length, height) - 1, thickness // 2)
        mask = np.zeros((2 * length + 1, 2 * height + 1), dtype=int)
        mask[length - thickness:length + thickness + 1, :] = 1
        mask[:, height - thickness:height + thickness + 1] = 1
        return mask

    def cross(self, length, thickness):
        thickness = min(max(1, thickness), length)
        mask = np.zeros((2 * length +  1, 2 * length + thickness), dtype=int)
        for i in range(0, 2 * length + 1):
            mask[i, i:i + thickness] = 1
            mask[i, 2 * length-i:2 * length + thickness-i] = 1
        return mask
    def pyramid(self, height):
        height = height + 1
        mask = np.zeros((height, height * 2 - 1), dtype=int)
        for i in range(height):
            mask[i, height - i -1:height + i] = 1
        return mask

    def diamond(self, length):
        length = length + 2
        mask = np.zeros((2 * length - 1, 2 * length - 1), dtype=int)
        for i in range(length):
            mask[i, length - i - 1:length + i] = 1
            mask[2 * length - i - 2, length - i - 1:length + i] = 1
        return mask

    def stair_step(self, height, length, steps, orientation = 0):
        steps = steps + 1
        mask = np.zeros((height * steps, length * steps), dtype=int)
        for i in range(steps):
            mask[i * height:i * height + height, :(i + 1) * length] = 1
        return np.rot90(mask, k = orientation)
    def zigzag(self, length, height, steps, orientation = 0):
        mask = np.zeros((length + 1, (length + 1) * (steps+2)), dtype=int)
        for i in range(steps + 2):
            for j in range(length + 1):
                if i % 2 == 0:
                    mask[j, i * (length) + j:i * (length) + j + min(height, length)] = 1
                else:
                    mask[length - j, i * (length) + j:i * (length) + j + min(height, length)] = 1
        return np.rot90(mask, k=orientation)
    def zigzag45(self, length, height, steps, orientation = 0):
        length = length + 1
        height = min(height, max(length//2, 1))
        mask = np.zeros(((steps)*(length-height)+length, (steps)*(length-height)+height), dtype = int)
        for j in range(steps + 1):
            mask[j * (length-height):j * (length-height) + length, j*(length-height):(j-1)*(length-height)+length] = 1
            mask[j * (length-height):j*(length-height) + height, (j-1)*(length-height):j*(length-height)+height] = 1
        return np.rot90(mask, k = orientation)
    def arrow(self, length, height, thickness, orientation=0):
        length = length + 1
        thickness = min(thickness, length)
        mask = np.zeros((length + 3 + height, 2 * length + 1), dtype=int)
        for i in range(length + 1):
            mask[i, length - i:length + i + 1] = 1
        mask[length + 1:length + 3 + height, length - thickness // 2:length + thickness // 2 + 1] = 1
        return np.rot90(mask, k=orientation)

    def maze(self, length, height):
        length = length + 6
        height = height + 6
        mask = np.zeros((height, length), dtype=int)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        def carve(x, y):
            mask[y, x] = 1
            dirs = directions[:]
            np.random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 0 <= nx < length and 0 <= ny < height and mask[ny, nx] == 0:
                    mask[y + dy, x + dx] = 1
                    carve(nx, ny)
        carve(np.random.randint(0, length), np.random.randint(0, height))
        return mask

    def spiral(self, length, height, orientation = 0, handedness = 0):
        length = length + 4
        height = height + 4
        mask = np.zeros((height, length), dtype=int)
        x, y = length // 2, height // 2
        mask[y, x] = 1
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        step = 2
        direction_index = 0
        while True:
            dx, dy = directions[direction_index]  # Current direction
            for _ in range(step):
                x += dx
                y += dy
                if not (0 <= x < length and 0 <= y < height):
                    return np.fliplr(np.rot90(mask, k=orientation)) if handedness == 1 else np.rot90(mask, k=orientation)
                mask[y, x] = 1
            direction_index = (direction_index + 1) % 4  # Rotate through directions
            if direction_index % 2 == 0:
                step += 2

    def v_shape(self, length, thickness, orientation=0):
        return self.zigzag(length, thickness, 0, orientation)

    def l_shape(self, length, height, thickness, orientation=0):
        if length < height:
            height = min(length * 3, height)
        else:
            length = min(height * 3 , length)
        thickness = max(min(max(1, thickness), min(height, length) // 2), 1)
        mask = np.zeros((length + 1, 1 + height), dtype=int)
        mask[:thickness, :] = 1
        mask[:, :thickness] = 1
        return np.rot90(mask, k=orientation)

    def t_shape(self, length, height, thickness, orientation=0):
        length = length + 1
        if length < height:
              height = math.floor(min(length, height // 1.5))
        else:
              length = math.floor(min(height, length // 1.5))
        thickness = max(min(max(1, thickness), height), 1)
        height = max(height + thickness, length//2)
        mask = np.zeros((height, length * 2 + 1), dtype=int)
        mask[:thickness, :] = 1
        mask[0:height, (length - thickness//2):(length + thickness//2 + 1)] = 1
        return np.rot90(mask, k=orientation)

    def motif(self, length, height, repeating_pattern):
        pattern_length, pattern_height = repeating_pattern.shape
        x_index = 0
        mask = np.zeros((length, height), dtype=int)
        print(mask.shape)
        for y in range(length):
            for x in range(height):
                mask[y, x] = repeating_pattern[y % pattern_length, x_index % pattern_height]
                x_index += 1
            x_index = x_index % pattern_height
        return mask


def display_grid(grid, title="Grid"):
    plt.imshow(grid)
    plt.title(title)
    plt.axis("off")
    plt.show()
