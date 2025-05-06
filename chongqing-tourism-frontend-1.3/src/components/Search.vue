//Search.vue

<template>
	<div id="container">
		<div class="error-message" v-if="errorMessage">
			{{errorMessage}}
		</div>
		<div id="myPageTop">
			<table>
				<tr>
					<td>
						<label style="font-size: 14px;">请输入要搜索的地点：</label>
					</td>
				</tr>
				<tr>
					<td>
						<input id="tipinput" />
					</td>
				</tr>
			</table>
		</div>
	</div>
</template>

<script>
	import AMapLoader from "@amap/amap-jsapi-loader";
	import axios from "axios";
	export default {
		props: {
			optimizedPath: {
				type: Array,
				default: () => [],
			},
		},
		data() {
			return {
				map: null,
				infoWindow: null,
				itineraryPoints: [],
				drivingList: [], // 存储多个 AMap.Driving 对象
				errorMessage: "",

			};
		},
		mounted() {
			this.initMap();
		},
		watch: {
			optimizedPath: {
				handler: 'handleOptimizedPathChange',
				immediate: true, // 立即执行一次
			},
		},
		methods: {
			handleOptimizedPathChange(newPath) {
				console.log('optimizedPath 发生变化（Search.vue）:', newPath);
				console.log("行程点数组:", this.itineraryPoints);
				AMapLoader.load({
					key: "bf9bd5e96adf1daae12a86c0430fc0a9",
					version: "2.0",
					plugins: [
						"AMap.Driving"
					],
				}).then((AMap) => {
					// 清除之前的路线
					this.clearPreviousRoutes();
					this.clearMarkers();
					console.log("新路径长度:", newPath.length);
					// 使用 AMap.Driving 服务规划路线
					for (let i = 0; i < newPath.length - 1; i++) {
						const startIdx = newPath[i];
						const endIdx = newPath[i + 1];
						// console.log("行程点数组:", this.itineraryPoints);
						// 从经纬度对象中获取经纬度值
						const startLngLat = [
							this.itineraryPoints[startIdx].position.lng,
							this.itineraryPoints[startIdx].position.lat,
						];
						const endLngLat = [
							this.itineraryPoints[endIdx].position.lng,
							this.itineraryPoints[endIdx].position.lat,
						];

						const driving = new AMap.Driving({
							map: this.map,
							autoFitView: false,
						});

						// 将 driving 对象存储在数组中
						this.drivingList.push(driving);

						// 执行路径规划
						driving.search(startLngLat, endLngLat, (status, result) => {
							if (status === "complete" && result.routes && result.routes.length) {
								console.log(`绘制驾车路线完成 (${startIdx} to ${endIdx})`);
							} else {
								this.errorMessage = "获取路线失败，请刷新页面后重试";
								console.error(
									`获取驾车数据失败 (${startIdx} to ${endIdx}):`,
									result
								);
							}
						});
					}
				});
			},

			initMap() {
				AMapLoader.load({
					key: "bf9bd5e96adf1daae12a86c0430fc0a9",
					version: "2.0",
					plugins: [
						"AMap.PlaceSearch",
						"AMap.AutoComplete",
						"AMap.Scale",
						"AMap.ControlBar",
						"AMap.MapType",
						"AMap.Driving"

					],
				}).then((AMap) => {
					this.map = new AMap.Map("container", {
						resizeEnable: true,
						zoom: 10,
						center: [106.551643, 29.562849],
					});

					this.map.addControl(new AMap.Scale());
					this.map.addControl(
						new AMap.ControlBar({
							position: {
								top: "10px",
								left: "10px",
							},
						})
					);
					this.map.addControl(
						new AMap.MapType({
							position: {
								bottom: "108px",
								right: "10px",
							},
						})
					);

					var autoOptions = {
						input: "tipinput",
						city: "023",
					};
					try {
						var auto = new AMap.AutoComplete(autoOptions);
						var placeSearch = new AMap.PlaceSearch({
							map: this.map,
						});
					} catch (e) {
						this.errorMessage = "获取相关地点失败，请刷新页面后重试";
					}

					auto.on("select", (e) => {
						this.map.setFitView();
						placeSearch.setCity(e.poi.adcode);
						placeSearch.search(e.poi.name);
					});

					// 创建信息窗体
					this.infoWindow = new AMap.InfoWindow({
						isCustom: true,
						offset: new AMap.Pixel(0, -30),
					});

					// 监听地图点击事件
					placeSearch.on("markerClick", (event) => {
						const marker = event.marker;
						this.openInfoWindow(event);
					});
				});
			},
			clearPreviousRoutes() {
				// 清除之前的路线
				for (const driving of this.drivingList) {
					driving.clear();
				}
				// 重置数组
				this.drivingList = [];
			},
			openInfoWindow(event) {
				const marker = event.marker;
				const position = marker.getPosition();
				const marker_name = event.data.name;
				const marker_address = event.data.address;

				// 使用原生 HTML+CSS 创建 InfoWindow 内容
				let info = [];
				info.push("<div class='info-window-content'>");
				info.push(`<p><strong>名称：</strong>${marker_name}</p>`);
				info.push(`<p><strong>地址：</strong>${marker_address}</p>`);
				info.push(`<button onclick='sendMessage(${position.lng}, ${position.lat})'>添加至行程</button>`);
				info.push("</div>");

				this.infoWindow = new AMap.InfoWindow({
					content: info.join(""), // 使用默认信息窗体框样式，显示信息内容
				});

				// 将 sendMessage 方法绑定到 window 对象中
				window.sendMessage = (lng, lat) => {
					this.addToItinerary({
						position: {
							lng: lng,
							lat: lat,
						},
						name: marker_name,
						address: marker_address,
					});
				};

				this.infoWindow.open(this.map, position);
			},
			addToItinerary(data) {
				// 添加到itineraryPoints
				try{
					this.itineraryPoints.push(data);
				console.log("行程点数组:", this.itineraryPoints);

				// 关闭信息窗体
				this.infoWindow.close();
				this.$emit("itinerary-updated", this.itineraryPoints);
				}catch(e){
					this.errorMessage = "添加地点失败，请刷新页面后重试";
				}
				
			},
			clearMarkers() {
				// 清除地图上的Marker
				this.map.clearMap();
			},

		},
	};
</script>

<style>
	#container {
		position: relative;
		width: 100%;
		height: 100%;
		z-index: 1;
	}

	#myPageTop {

		position: absolute;
		top: 10px;
		right: 10px;
		background-color: white;
		border-radius: 5px;
		box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 5px;
		z-index: 2;

	}

	/* 添加一个样式用于 infoWindow 的内容 */
	.info-window-content {
		padding: 10px;
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
</style>