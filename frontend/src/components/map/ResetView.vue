<template>
  <div class="reset mapboxgl-ctrl-group mapboxgl-ctrl" title="Reset map" v-if="aoi && maximized" @click="resetMap()">
    <b-icon-bootstrap-reboot id="icon" scale=1.6 aria-hidden="true"></b-icon-bootstrap-reboot>
  </div>
</template>
<script>
import { runFilter } from "@/components/filters";
import mapboxgl from "mapbox-gl";
class ResetControl {
  constructor(el){
    this._container = el;
  }
  onAdd(map) {
    this._map = map;
    return this._container;
  }
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
    }
  }
export default {
  props: ["map", "maximized"],
  data(){
    return {
      control: null,
      resetIcon: ["fas", "redo"]
    }
  },
  computed: {
    aoi(){
      return this.$store.getters["maps/getSelectedAoi"];
    },
    selectedFeature() {
      return this.$store.getters["maps/getSelectedFeature"];
    },
    customAnalysis(){
      return this.$store.getters['analysis/getCustomAnalysis'];
    }
  },
  methods: {
    resetMap(){
      if(this.selectedFeature){
        this.$store.dispatch("maps/clearSelectedFeature", {vm: this});
        this.$root.$emit('analysis-close');
      }
      if(this.customAnalysis){
        this.$store.dispatch("analysis/clearCustomAnalysis");
        this.$root.$emit('custom-analysis-close');
      }
      let bounds = new mapboxgl.LngLatBounds(this.aoi.extent);
      this.map.fitBounds(bounds,
        {padding: { top: 60, right: 0, left: 200, bottom: 20 }},
        {source: 'reset-map'}
      );
      this.$root.$emit('reset-map');
    }
  },
  watch: {
    map(){
      if(this.map){
        var scale = new mapboxgl.ScaleControl();
        this.map.addControl(scale, "bottom-right");
        this.control = new ResetControl(this.$el);
        this.map.addControl(this.control, 'bottom-right');
      }
    }
  }
}
</script>
<style scoped>
.reset {
  width: 30px;
  height: 30px;
  margin: 0 10px 10px 0;
  font-size: 12px;
  background-color: white;
  border: 0;
  border-radius: 5px;
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  z-index: 500;
}
.reset:hover {
  background-color: #f1f1f1;
}
#icon {
  position: relative;
  top: 6px;
  left: 9px;
}
</style>
