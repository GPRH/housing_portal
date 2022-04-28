<template>
  <div id="map" :class="maximized ? 'maximized' : 'minimized'">
    <app-switcher :maximized="maximized"></app-switcher>
    <app-map-indicator :maximized="maximized"></app-map-indicator>
    <app-mapillary-warning :map="map" :maximized="maximized"></app-mapillary-warning>
  </div>
</template>
<script>
import Switcher from "@/components/mapillary/Switcher"
import MapIndicator from "@/components/map/MapIndicator";
import MapillaryWarning from "@/components/mapillary/MapillaryWarning";
export default {
  props: ["map", "maximized"],
  components: {
    appSwitcher: Switcher,
    appMapIndicator: MapIndicator,
    appMapillaryWarning: MapillaryWarning
  },
  created(){
    this.$root.$on('toggle-mapillary', () => {
      this.map.resize();
    })
  }
};
</script>
<style>
#map.maximized {
  position: absolute;
  left: 0;
  top: 0;
  height: 100vh !important;
  width: 100vw !important;
  font-family: 'Roboto Medium', sans-serif;
  padding: 0px;
}
#map.minimized {
  position: absolute;
  left: 22px;
  top: calc(100vh - 275px);
  width: 320px;
  height: 240px;
  z-index: 1201;
  /* border-radius: 8px;
  border: 1px solid lightgrey; */
  -webkit-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
}
#map.minimized .mapboxgl-canvas {
  /* border-radius: 8px; */
}


@media (max-width: 768px) {
  #map.minimized {
    position: absolute;
    left: 20px;
    top: calc(100vh - 220px);
    width: 280px;
    height: 180px;
  }
}

.mapboxgl-ctrl-geocoder {
  position: absolute;
  top: 50px;
  max-width: 300px !important;
}
.mapboxgl-ctrl-attrib {
  font-size: 12px !important;
}

.popup .mapboxgl-popup-content {
  border-radius: 8px;
  padding-top: 15px;
  max-width: 150px;
  max-height: 75px;
  opacity: .9;
}
.popup .mapboxgl-popup-tip {
  opacity: 0.9;
}
.popup .gs-popup-title {
  font: 600 15px/22px Sans-serif;
  /* font-size: 1.2em; */
}
</style>
