# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理跨域请求
from solve_tsp import perform_optimization  # 导入路径优化算法

app = Flask(__name__)
CORS(app)  # 启用CORS，允许跨域请求


@app.route('/optimize', methods=['POST'])
def optimize_route():
    data = request.get_json()
    city_coords = data.get('city_coords', [])
    distances = data.get('distances', [])
    entrance_index = data.get('entrance_index')
    exit_index = data.get('exit_index')

    if len(city_coords) == 2:
        return jsonify({'optimized_path': [entrance_index, exit_index]})
    if len(city_coords) == 3:
        middle_index = 3 - entrance_index - exit_index  # 找到中间点的索引
        optimized_path = [entrance_index, middle_index, exit_index]
        return jsonify({'optimized_path': optimized_path})
    else:
        # 调用路径优化算法
        optimized_route = perform_optimization(city_coords, distances, entrance_index, exit_index)
        # 转换为 Python 内置的列表类型
        optimized_route_list = list(map(int, optimized_route))

    return jsonify({'optimized_path': optimized_route_list})


if __name__ == '__main__':
    app.run(debug=True)
