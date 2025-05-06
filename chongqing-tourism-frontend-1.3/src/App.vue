//App.vue

<template>
	<div id="app">
		<div class="map">
			<!-- 使用 Search 组件 -->
			<Search :optimizedPath="optimizedPath" @itinerary-updated="updateItineraryPoints" />
		</div>
		<div class="sidebar">
			<!-- 使用 Itinerary 组件 -->
			<Itinerary :itineraryPoints="itineraryPoints" @optimizedPath-updated="updateOptimizedPath"
				@entrance-updated="updateEntrancePoint" @exit-updated="updateExitPoint" />
		</div>
	</div>
</template>

<script>
	import Search from './components/Search.vue';
	import Itinerary from './components/Itinerary.vue';

	export default {
		components: {
			Search,
			Itinerary,
		},
		data() {
			return {
				itineraryPoints: [], // 存储用户选择的景点信息，包括名称和地址
				optimizedPath: [],
				entrancePoint: null,
				exitPoint: null,
			};
		},
		methods: {
			updateItineraryPoints(itineraryPoints) {
				// 更新父组件中的itineraryPoints
				this.itineraryPoints = itineraryPoints;
			},
			updateEntrancePoint(point) {
				// 更新父组件中的entrancePoint
				this.entrancePoint = point;
			},
			updateExitPoint(point) {
				// 更新父组件中的exitPoint
				this.exitPoint = point;
				console.log('exitPoint 发生变化(父组件):', this.exitPoint);
			},
			updateOptimizedPath(optimizedPath) {
				this.optimizedPath = optimizedPath;
				console.log('optimizedPath 发生变化(父组件):', this.optimizedPath);
			},
		},
	};
</script>

<style>
	/* 在这里编写全局样式 */
	#app {
		display: flex;
		position: absolute;
		height: 100%;
		width: 100%;
	}

	.map {
		width: 80%;

	}

	.sidebar {
		width: 15%;
		padding-left: 2%;
	}
</style>