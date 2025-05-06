# solve_tsp.py

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from acowithsa.ant_colony import AntColony
from acowithsa.simulated_annealing import SimulatedAnnealing
import time


def perform_optimization(city_coords, distances, entrance_index, exit_index):
    save_data_to_file("examples/data.txt",
                      city_coords, distances)
    return main(entrance_index=entrance_index, exit_index=exit_index)


def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 读取城市坐标和邻接矩阵
    city_coords = []
    distances = []
    for line in lines:
        data = list(map(float, line.strip().split()))
        city_coords.append(data[:2])
        distances.append(data[2:])

    return np.array(city_coords), np.array(distances)


def save_data_to_file(file_path, city_coords, distances):
    with open(file_path, 'w') as file:
        # 保存接收的城市坐标和邻接矩阵
        for i in range(len(city_coords)):
            line = f"{city_coords[i][0]} {city_coords[i][1]} {' '.join(map(str, distances[i]))}\n"
            file.write(line)


# def generate_random_data(num_cities, x_range=(0, 100), y_range=(0, 100)):
#     city_coords = np.random.uniform(0, 100, (num_cities, 2))
#     distances = np.random.uniform(0, 141.421356, size=(num_cities, num_cities))
#     np.fill_diagonal(distances, 0)
#     distances = (distances + distances.T) / 2.0
#     return city_coords, distances


def generate_random_data(num_cities, x_range=(0, 100), y_range=(0, 100)):
    # 生成城市坐标
    city_coords = np.random.uniform(x_range[0], x_range[1], (num_cities, 2))

    # 计算城市之间的欧几里得距离
    distances = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            distances[i][j] = np.linalg.norm(city_coords[i] - city_coords[j])

    return city_coords, distances


def main(num_cities=10, num_runs=1, entrance_index=1, exit_index=3):
    global city_coords, distances, ant_colony_path, optimized_path
    total_optimization_rate = 0.0
    total_run_time = 0.0

    for _ in tqdm(range(num_runs), desc="Total Progress"):
        # 记录开始时间
        start_time = time.time()

        # 从文件读取或生成数据
        try:
            city_coords, distances = read_data_from_file("examples/data.txt")
        except FileNotFoundError:
            print(f"File not found. Generating random data with {num_cities} cities.")
            city_coords, distances = generate_random_data(num_cities)
            if num_runs == 1:
                save_data_to_file("examples/temp.txt", city_coords, distances)

        # 蚁群算法
        ant_colony = AntColony(distances, num_ants=5, alpha=2.0, beta=3.0, rho=0.5, Q=100, entrance=entrance_index,
                               exit=exit_index)
        ant_colony_path = ant_colony.run(num_iterations=100)

        # 模拟退火算法优化
        simulated_annealing = SimulatedAnnealing(ant_colony_path, distances, initial_temperature=400,
                                                 cooling_rate=0.9998,
                                                 min_temperature=1, max_iterations=50000)
        optimized_path = simulated_annealing.run()
        # 记录结束时间
        end_time = time.time()

        # 计算运行时间
        run_time = end_time - start_time
        total_run_time += run_time

        # 计算优化率并累加
        ant_colony_distance_before = ant_colony.calculate_total_distance(ant_colony_path)
        optimized_distance = ant_colony.calculate_total_distance(optimized_path)
        optimization_rate = (ant_colony_distance_before - optimized_distance) / ant_colony_distance_before * 100
        total_optimization_rate += optimization_rate

    # 计算平均优化率和平均运行时间
    average_optimization_rate = total_optimization_rate / num_runs
    average_run_time = total_run_time / num_runs
    print(f"Best path: {optimized_path}")
    print(f"Average Optimization Rate over {num_runs} runs: {average_optimization_rate:.2f}%")
    print(f"Average Run Time over {num_runs} runs: {average_run_time:.2f} seconds")

    if num_runs == 1:
        plot_tsp_solution(city_coords, ant_colony_path, distances, title="Ant Colony Algorithm Solution")
        plot_tsp_solution(city_coords, optimized_path, distances, title="Optimized Solution after Simulated Annealing")

    return optimized_path


def plot_tsp_solution(city_coords, path, distances, title="TSP Solution"):
    y = [coord[0] for coord in city_coords]
    x = [coord[1] for coord in city_coords]

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, c='red', marker='o', label='Cities')

    # 依据路径连接城市
    for i in range(len(path) - 1):
        plt.plot([x[path[i]], x[path[i + 1]]], [y[path[i]], y[path[i + 1]]], 'k-')
        # 添加标签，显示距离
        distance_label = f"{distances[path[i]][path[i + 1]]:.2f}"
        plt.text((x[path[i]] + x[path[i + 1]]) / 2, (y[path[i]] + y[path[i + 1]]) / 2, distance_label,
                 fontsize=8, color='blue')

    # 添加标签，显示距离
    distance_label = f"{distances[path[-1]][path[0]]:.2f}"
    plt.text((x[path[-1]] + x[path[0]]) / 2, (y[path[-1]] + y[path[0]]) / 2, distance_label,
             fontsize=8, color='blue')

    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
