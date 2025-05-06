//Itinerary

<template>

	<div>
		<div>
			<label>选择进入地点：</label>
			<select v-model="entrancePoint" @change="updateEntrancePoint">
				<option v-for="(point, index) in itineraryPoints" :key="index" :value="index">
					{{ point.name }}
				</option>
			</select>
		</div>
		<div>
			<label>选择离开地点：</label>
			<select v-model="exitPoint" @change="updateExitPoint">
				<option v-for="(point, index) in itineraryPoints" :key="index" :value="index">
					{{ point.name }}
				</option>
			</select>
		</div>
		<h2>旅行清单</h2>
		<ul style="margin-left: -20px;">
			<li v-for="(point, index) in itineraryPoints" :key="index">
				<div class="itinerary-item">
					<span class="itinerary-text" :title="point.name + ' - ' + point.address">{{ point.name }}</span>
					<button @click="removePoint(index)">删除</button>
				</div>
			</li>
		</ul>
		<button @click="generatePath">生成路径</button>
		<div class="error-message" v-if="errorMessage">
			{{errorMessage}}
		</div>
		<div class="what-is-going-on" v-if="whatIsGoingOn">
			{{whatIsGoingOn}}
		</div>
		<div v-if="optimizedPath.length > 0">
			<h2>最佳路径</h2>
			<ul>
				<li v-for="(index, i) in optimizedPath" :key="i">
					{{ i + 1 }}. {{ itineraryPoints[index].name }}
				</li>
			</ul>
		</div>

	</div>

</template>

<script>
	import AMapLoader from "@amap/amap-jsapi-loader";
	import axios from "axios"; // Import axios

	export default {
		props: {
			itineraryPoints: {
				type: Array,
				default: () => [],
			},
		},
		data() {
			return {
				distanceMatrix: [], // 存储距离矩阵
				optimizedPath: [],
				entrancePoint: null,
				exitPoint: null,
				errorMessage:"",
				whatIsGoingOn:"",
			};
		},
		methods: {
			updateEntrancePoint() {
				this.$emit("entrance-updated", this.itineraryPoints[this.entrancePoint]);
			},
			updateExitPoint() {
				this.$emit("exit-updated", this.itineraryPoints[this.exitPoint]);
			},
			updateOptimizedPath() {

				this.$emit("optimizedPath-updated", this.optimizedPath);
			},

			generatePath() {
				
				if (this.itineraryPoints.length < 2) {
					this.errorMessage="请将至少两个地点添加至行程";
					setTimeout(() => {
					      this.errorMessage = ""; // 2 秒后清空错误消息
					    }, 2000);
					console.log(this.errorMessage);
					return;
				}else if(this.itineraryPoints.length >= 2&&this.entrancePoint==null){
					this.errorMessage="请选择起点";
					setTimeout(() => {
					      this.errorMessage = ""; // 2 秒后清空错误消息
					    }, 2000);
					console.log(this.errorMessage);
					return;
				}else if(this.itineraryPoints.length >= 2&&this.exitPoint==null){
					console.log('entrancePoint:',this.entrancePoint);
					console.log('exitPoint:',this.exitPoint);
					this.errorMessage="请选择终点";
					setTimeout(() => {
					      this.errorMessage = ""; // 2 秒后清空错误消息
					    }, 2000);
					console.log(this.errorMessage);
					return;
				}else if(this.itineraryPoints.length >= 2&&this.entrancePoint&&this.exitPoint==null){
					this.errorMessage="请选择起点和终点";
					setTimeout(() => {
					      this.errorMessage = ""; // 2 秒后清空错误消息
					    }, 2000);
					console.log(this.errorMessage);
					return;
				}
				// 在生成路径按钮点击时获取距离矩阵
				
				this.calculateRoutes(this.itineraryPoints).then(() => {
					this.whatIsGoingOn="正在计算路线";
					const cityCoords = this.itineraryPoints.map(point => [point.position.lat, point.position.lng]);
					const entranceCoords = this.itineraryPoints[this.entrancePoint].position;
					const exitCoords = this.itineraryPoints[this.exitPoint].position;
					const dataToSend = {
						city_coords: this.itineraryPoints.map(point => [point.position.lat, point.position
							.lng
						]),
						distances: this.distanceMatrix,
						entrance_index: this.entrancePoint,
						exit_index: this.exitPoint,
					};
					console.log('向后端发送数据:', dataToSend);
					// 发送 dataToSend 到后端
					axios.post('http://localhost:5000/optimize', dataToSend)
						.then(response => {
							// 处理成功的响应
							console.log('后端返回的数据:', response.data);
							this.optimizedPath = response.data.optimized_path;
							this.whatIsGoingOn="";
							this.updateOptimizedPath();
						})
						.catch(error => {
							// 处理错误
							console.error('发生错误:向后端传输数据失败', error);
							this.whatIsGoingOn="";
							this.errorMessage = '向后端传输数据失败，请尝试刷新页面后重试。';
						});
				});
				
			},
			async calculateRoutes(points) {
				// 使用异步加载
				await AMapLoader.load({
					key: 'bf9bd5e96adf1daae12a86c0430fc0a9', // 替换为你的高德地图API Key
					version: '2.0',
					plugins: ['AMap.Driving'],
				});

				this.distanceMatrix = Array.from({
					length: points.length
				}, () => Array(points.length).fill(0));
				this.whatIsGoingOn="正在获取地理数据";
				for (let i = 0; i < points.length; i++) {
					for (let j = i + 1; j < points.length; j++) {
						const start = [points[i].position.lng, points[i].position.lat];
						const end = [points[j].position.lng, points[j].position.lat];
						const distance = await this.calculateRouteBetweenPoints(start, end);

						this.distanceMatrix[i][j] = distance;
						this.distanceMatrix[j][i] = distance;
					}
				}
				this.whatIsGoingOn="";
				console.log('距离矩阵:', this.distanceMatrix);
					
			},
			calculateRouteBetweenPoints(start, end) {
				return new Promise((resolve, reject) => {
					// 使用异步加载
					AMapLoader.load({
						key: 'bf9bd5e96adf1daae12a86c0430fc0a9', // 替换为你的高德地图API Key
						version: '2.0',
						plugins: ['AMap.Driving'],
					}).then((AMap) => {
						const driving = new AMap.Driving({
							policy: AMap.DrivingPolicy.LEAST_TIME,
						});

						driving.search(start, end, (status, result) => {
							if (status === 'complete') {
								const distance = result.routes[0].distance;
								resolve(distance);
							} else {
								console.error('发生错误：获取地理数据失败失败:', result);
								this.whatIsGoingOn="";
								this.errorMessage = '获取地理数据失败，请尝试刷新页面后重试。';
							}
						});
					});
				});
			},
			removePoint(index) {
				console.log('尝试删除itineraryPoints:', index);
				console.log('itineraryPoints:', this.itineraryPoints);
				this.itineraryPoints.splice(index, 1);
			},
		},
	};
</script>

<style scoped>
	.itinerary-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-left: ;
	}

	.itinerary-text {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		max-width: 300px;
		cursor: pointer;
	}

	.itinerary-text:hover {
		z-index: 1;
		background-color: #fff;
	}

	.error-message {
		position: fixed;
		top: 20px;
		left: 50%;
		transform: translateX(-50%);
		background-color: #ffcccc;
		color: #ff0000;
		padding: 10px 20px;
		border-radius: 5px;
		border: 1px solid #ff0000;
		z-index: 3;
	}
	.what-is-going-on {
		position: fixed;
		top: 20px;
		left: 50%;
		transform: translateX(-50%);
		background-color: #d9ffdc;
		color: #00aa7f;
		padding: 10px 20px;
		border-radius: 5px;
		border: 1px solid #00aa7f;
		z-index: 3;
	}
</style>