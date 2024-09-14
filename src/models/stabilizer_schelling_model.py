import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StabilizerSchellingModel:
    def __init__(self) -> None:
        self.grid_size = 20
        self.num_agents = 100
        self.num_stabilizers = 20
        self.similarity_threshold = 0.4
        self.iteration = 500

    def initialize_grid(self, grid_size, num_agents, num_stabilizers):
        grid = np.full((grid_size, grid_size), None)

        agents = ["P"] * (num_agents // 2) + ["E"] * (num_agents // 2)
        stabilizers = ["S"] * num_stabilizers

        random.shuffle(agents)
        random.shuffle(stabilizers)

        positions = random.sample(
            range(grid_size * grid_size), num_agents + num_stabilizers
        )

        for pos, agent in zip(positions[:num_agents], agents):
            x, y = divmod(pos, grid_size)
            grid[x, y] = agent

        for pos in positions[num_agents:]:
            x, y = divmod(pos, grid_size)
            grid[x, y] = "S"

        return grid

    def calculate_satisfaction(self, grid, x, y):
        agent = grid[x, y]
        neighbors = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                    neighbors.append(grid[nx, ny])

        if len(neighbors) == 0:
            return 1

        similar_neighbors = sum(
            1 for neighbor in neighbors if neighbor == agent or neighbor == "S"
        )
        return similar_neighbors / len(neighbors)

    def move_agents(self, grid):
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] is not None and grid[x, y] != "S":
                    satisfaction = self.calculate_satisfaction(grid, x, y)
                    if satisfaction < self.similarity_threshold:
                        empty_positions = np.argwhere(grid == None)
                        if empty_positions.size > 0:
                            new_pos = random.choice(empty_positions)
                            grid[new_pos[0], new_pos[1]] = grid[x, y]
                            grid[x, y] = None

    def update(self, frame, grid, img, texts):
        self.move_agents(grid)

        data = np.ones((self.grid_size, self.grid_size, 3)) * 0.9

        data[grid == "P"] = [0, 0, 1]  # Blue
        data[grid == "E"] = [1, 0, 0]  # Red
        data[grid == "S"] = [0.5, 1, 0.5]  # Green

        img.set_data(data)

        for t in texts:
            t.remove()
        texts.clear()

        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if grid[x, y] is not None:
                    text = plt.text(
                        y,
                        x,
                        grid[x, y],
                        ha="center",
                        va="center",
                        color="white" if grid[x, y] != "S" else "black",
                        fontsize=8,
                        fontweight="bold",
                    )
                    texts.append(text)

        return (img,) + tuple(texts)

    def run_animation(self):
        grid = self.initialize_grid(
            self.grid_size, self.num_agents, self.num_stabilizers
        )

        fig, ax = plt.subplots()

        img = ax.imshow(
            np.ones((self.grid_size, self.grid_size, 3)) * 0.9, interpolation="nearest"
        )
        ax.set_title("Schelling Model - Neighborhood Segregation with Stabilizers")
        ax.axis("off")

        texts = []

        animation = FuncAnimation(
            fig,
            self.update,
            fargs=(grid, img, texts),
            frames=self.iteration,
            repeat=False,
            interval=500,
        )

        animation.save(
            "plots/schelling_model_stabilizers_small.mp4", writer="ffmpeg", fps=50
        )

    def run(self):
        self.run_animation()
