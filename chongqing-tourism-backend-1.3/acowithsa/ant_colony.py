# ant_colony.py
import numpy as np
from tqdm import tqdm


class AntColony:
    def __init__(self, distances, num_ants, alpha=2.0, beta=3.0, rho=0.5, Q=100, entrance=None, exit=None):
        self.distances = distances
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.pheromone = np.ones_like(distances)
        self.entrance = entrance
        self.exit = exit

    def generate_ant_path(self):
        start_city = self.entrance if self.entrance is not None else np.random.randint(len(self.distances))
        visited_cities = [start_city]
        current_city = start_city

        while len(visited_cities) < len(self.distances):
            next_city = self.select_next_city(current_city, visited_cities)
            visited_cities.append(next_city)
            current_city = next_city

        # 如果指定了退出点，请确保路径以退出点结束
        if self.exit is not None and visited_cities[-1] != self.exit:
            visited_cities.append(self.exit)

        return visited_cities

    def select_next_city(self, current_city, visited_cities):
        pheromone_values = self.pheromone[current_city]
        heuristic_values = self.calculate_heuristic_values(current_city, visited_cities)

        probabilities = (pheromone_values ** self.alpha) * (heuristic_values ** self.beta)
        if len(visited_cities) < len(self.distances) - 1:
            # 将退出点的概率设置为零
            probabilities[self.exit] = 0

        # 归一化概率
        probabilities /= np.sum(probabilities)

        next_city = np.random.choice(range(len(self.distances)), p=probabilities)

        return next_city

    def calculate_heuristic_values(self, current_city, visited_cities):
        heuristic_values = np.zeros(len(self.distances))

        for city in range(len(self.distances)):
            if city not in visited_cities:
                distance = self.distances[current_city][city]
                heuristic_values[city] = 1 / distance if distance != 0 else 0

        return heuristic_values

    def update_pheromone(self, paths, Q, rho):
        self.pheromone *= (1 - rho)

        for path in paths:
            path_distance = self.calculate_total_distance(path)
            for i in range(len(path) - 1):
                self.pheromone[path[i]][path[i + 1]] += Q / path_distance
                self.pheromone[path[i + 1]][path[i]] += Q / path_distance

        self.pheromone[self.pheromone < 0] = 0

    def run(self, num_iterations):
        best_path = None
        best_distance = float('inf')

        for iteration in tqdm(range(num_iterations), desc="Ant Colony Progress"):
            paths = [self.generate_ant_path() for _ in range(self.num_ants)]

            for path in paths:
                distance = self.calculate_total_distance(path)
                if distance < best_distance:
                    best_distance = distance
                    best_path = path

            if best_path is not None:
                self.update_pheromone(paths, Q=100, rho=0.5)

        return best_path

    def calculate_total_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i]][path[i + 1]]
        total_distance += self.distances[path[-1]][path[0]]
        return total_distance
