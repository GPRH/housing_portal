<template>
  <b-alert v-if="show && map" id="debug-tool" variant="dark" show>
    <div>Zoom level: {{ zoom }}</div>
    <div>Mapbox zoom: {{ mapboxZoom }}</div>
    <b-form-checkbox  class="switcher float-left" v-model="boundaries" @input="showBoundaries()" switch>
      <span class="switcher-label">Tile Boundaries</span>
    </b-form-checkbox>
    <!-- <b-form-checkbox  v-if="aoi" class="switcher float-left" v-model="mapillary" @input="toggleMapillary()" switch>
      <span class="switcher-label">Mapillary Layers</span>
    </b-form-checkbox> -->
  </b-alert>
</template>
<script>
export default {
  props: ["map"],
  data(){
    return {
      boundaries: false,
      mapillary: false,
    }
  },
  computed: {
    aoi() {
      return this.$store.getters["maps/getSelectedAoi"];
    },
    show(){
      return process.env.NODE_ENV === 'development';
    },
    zoom(){
      return this.map && this.map.getZoom() < 14 ? null : Math.round(this.map.getZoom() - 13, 2);
    },
    mapboxZoom(){
      return Math.round(this.map.getZoom(), 2);
    }
  },
  methods: {
    showBoundaries(){
      this.map.showTileBoundaries = this.boundaries;
    },
    toggleMapillary(){
      let visible = this.mapillary ? "visible" : "none";
      this.map.setLayoutProperty('mapillary-sequences', "visibility", visible);
      this.map.setLayoutProperty('mapillary-images', "visibility", visible);
    }
  }
}
</script>
<style scoped>
#debug-tool {
  position: absolute;
  top: 50px;
  right: 8px;
  width: 200px;
  pointer-events: all;
  z-index: 1100;
}
.switcher, .switcher-label {
  cursor: pointer !important;
  font-size: .95em;
}
</style>
