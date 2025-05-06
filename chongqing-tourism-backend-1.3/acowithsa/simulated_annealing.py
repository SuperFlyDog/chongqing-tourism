# simulated_annealing.py
import numpy as np
from tqdm import tqdm


class SimulatedAnnealing:
    def __init__(self, initial_path, distances, initial_temperature=100, cooling_rate=0.99, min_temperature=1,
                 max_iterations=2000):
        self.initial_path = initial_path
        self.distances = distances
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.max_iterations = max_iterations

    def run(self):
        current_path = self.initial_path
        current_distance = self.calculate_total_distance(current_path)
        best_path = current_path
        best_distance = current_distance
        temperature = self.initial_temperature

        for iteration in tqdm(range(self.max_iterations), desc="Simulated Annealing Progress"):
            new_path = self.generate_neighbor_path(current_path)
            new_distance = self.calculate_total_distance(new_path)

            if self.accept_new_solution(current_distance, new_distance, temperature):
                current_path = new_path
                current_distance = new_distance

                if current_distance < best_distance:
                    best_path = current_path
                    best_distance = current_distance

            temperature *= self.cooling_rate

            if temperature <= self.min_temperature:
                break

        return best_path

    def generate_neighbor_path(self, path):
        neighbor_path = path.copy()
        # 随机交换两个地点（除开起点和终点）
        last_index = len(path) - 1
        index1, index2 = np.random.choice([i for i in range(len(path)) if i != 0 and i != last_index], size=2,
                                          replace=False)

        neighbor_path[index1], neighbor_path[index2] = neighbor_path[index2], neighbor_path[index1]

        return neighbor_path

    def accept_new_solution(self, current_distance, new_distance, temperature):
        if new_distance < current_distance:
            return True
        else:
            probability = np.exp((current_distance - new_distance) / temperature)
            return np.random.rand() < probability

    def calculate_total_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i]][path[i + 1]]
        total_distance += self.distances[path[-1]][path[0]]
        return total_distance
