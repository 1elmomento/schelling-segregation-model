import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class StabilizerSchellingModelWithCost:
    def __init__(self) -> None:
        self.grid_size = 20
        self.num_agents = 100
        self.num_stabilizers = 20  # Number of stabilizer agents
        self.similarity_threshold = 0.4
        self.iteration = 500
        self.moving_cost_factor = 0.1  # Higher values increase moving costs
        self.max_move_radius = 5  # Maximum move distance radius
        self.min_improvement_threshold = (
            0.05  # Threshold for improvement to avoid oscillation
        )

    def initialize_grid(self, grid_size, num_agents, num_stabilizers):
        grid = np.full((grid_size, grid_size), None)

        # Create lists for agents: half "P", half "E", and "S" stabilizers
        agents = ["P"] * (num_agents // 2) + ["E"] * (num_agents // 2)
        stabilizers = ["S"] * num_stabilizers  # Adding stabilizer agents

        # Shuffle both lists
        random.shuffle(agents)
        random.shuffle(stabilizers)

        # Sample unique random positions for all agents and stabilizers
        positions = random.sample(
            range(grid_size * grid_size), num_agents + num_stabilizers
        )

        # Place agents on the grid
        for pos, agent in zip(positions[:num_agents], agents):
            x, y = divmod(pos, grid_size)
            grid[x, y] = agent

        # Place stabilizer agents on the grid
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

        # Stabilizers ("S") do not affect satisfaction negatively
        similar_neighbors = sum(
            1 for neighbor in neighbors if neighbor == agent or neighbor == "S"
        )
        return similar_neighbors / len(neighbors)

    def move_agents(self, grid):
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                if (
                    grid[x, y] is not None and grid[x, y] != "S"
                ):  # Stabilizers don't move
                    satisfaction = self.calculate_satisfaction(grid, x, y)
                    if satisfaction < self.similarity_threshold:
                        # Get positions within the move radius
                        nearby_empty_positions = [
                            (new_x, new_y)
                            for new_x in range(
                                max(0, x - self.max_move_radius),
                                min(self.grid_size, x + self.max_move_radius + 1),
                            )
                            for new_y in range(
                                max(0, y - self.max_move_radius),
                                min(self.grid_size, y + self.max_move_radius + 1),
                            )
                            if grid[new_x, new_y] is None
                        ]

                        if nearby_empty_positions:
                            best_new_pos = None
                            best_improvement = -float("inf")
                            current_satisfaction = satisfaction

                            for new_x, new_y in nearby_empty_positions:
                                new_satisfaction = self.calculate_satisfaction(
                                    grid, new_x, new_y
                                )
                                # Calculate Manhattan distance
                                distance = abs(new_x - x) + abs(new_y - y)
                                moving_cost = self.moving_cost_factor * distance
                                improvement = (
                                    new_satisfaction - current_satisfaction
                                ) - moving_cost

                                # Choose the move that provides the best improvement
                                if improvement > best_improvement:
                                    best_improvement = improvement
                                    best_new_pos = (new_x, new_y)

                            # Move only if there's substantial improvement
                            if (
                                best_new_pos
                                and best_improvement > self.min_improvement_threshold
                            ):
                                grid[best_new_pos[0], best_new_pos[1]] = grid[x, y]
                                grid[x, y] = None

    def update(self, frame, grid, img, texts):
        self.move_agents(grid)

        # Light gray background
        data = np.ones((self.grid_size, self.grid_size, 3)) * 0.9

        # "P" agents are blue (0, 0, 1), "E" agents are red (1, 0, 0), "S" agents are light green (0.5, 1, 0.5)
        data[grid == "P"] = [0, 0, 1]
        data[grid == "E"] = [1, 0, 0]
        data[grid == "S"] = [0.5, 1, 0.5]  # Light green for stabilizers

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
        ax.set_title("Schelling Model - Neighborhood Segregation with Moving Cost")
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

        animation.save("plots/schelling_model_moving_cost.mp4", writer="ffmpeg", fps=50)

    def run(self):
        self.run_animation()
