<template>
  <div id="draw" v-if="maximized" class="d-flex align-items-center justify-content-left w-100">
      <span id="title" :class="isDrawing ? 'drawing': ''">Analyze custom area</span>
      <b-icon-bounding-box font-scale="1.1" id="bbox-draw" title="Draw Polygon" :class="{ loading: loading }" @click="startDraw()"></b-icon-bounding-box>
      <b-icon-trash-fill font-scale="1.1" id="cancel-draw" title="Cancel Analysis" :class="{ loading: loading}" @click="cancelDraw()"></b-icon-trash-fill>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import drawStyles from "./styles";
import { resetBuildings } from "@/components/map"
import { selectAoi } from "@/components/map/events";
import * as _ from "lodash";
export default {
  props: ["map", "maximized"],
  data() {
    return {
      draw: null,
      hasDrawControl: false,
      loading: false,
      searching: false,
      isDrawing: false,
  }
  },
  methods: {
    startDraw(){
      this.$store.dispatch("maps/clearSelectedFeature", { vm: this });
      this.$store.dispatch("filters/clearFilters");
      this.map.setFilter('buildings', null);
      this.map.setFilter('building-outlines', null);
      resetBuildings(this);
      this.addDrawControl();
      this.draw.deleteAll();
      this.$store.dispatch("analysis/clearCustomAnalysis");
      this.draw.changeMode('draw_polygon');
      this.$root.$emit('draw-started');
      this.isDrawing = true;
    },
    cancelDraw(){
      if(this.hasDrawControl){
        this.close();
        this.$root.$emit('draw-cancelled');
        this.isDrawing = false;
      }
    },
    closeDraw(){
      if(this.hasDrawControl){
        this.close()
        this.$root.$emit('draw-stopped');
        this.isDrawing = false;
      }
    },
    close(){
      this.draw.deleteAll();
      this.draw.changeMode('simple_select');
      this.$store.dispatch("analysis/clearCustomAnalysis");
      this.$store.dispatch("filters/clearFilters");
      this.map.setFilter('buildings', null);
      this.map.setFilter('building-outlines', null);
      resetBuildings(this);
      this.removeDrawControl();
      let aoiFeature = this.$store.getters["maps/getSelectedAoi"].feature;
      selectAoi(this, aoiFeature.feature, true);
    },
    addDrawControl(){
      if(!this.hasDrawControl){
        this.draw = new MapboxDraw({
          displayControlsDefault: false,
          styles: drawStyles
        });
        this.map.addControl(this.draw);
        this.hasDrawControl = true;
      }
    },
    removeDrawControl(){
      if(this.hasDrawControl){
        this.map.removeControl(this.draw);
        this.hasDrawControl = false;
      }
    }
  },
  computed: {
    ...mapGetters({
      displayLayers: "maps/getDisplayLayers",
      selectedFeature: "maps/getSelectedFeature"
    }),
    displayDrawControls(){
      let buildings = _.filter(this.displayLayers, layer => {
        return layer.id === 'buildings' && layer.checked === true;
      })
      return buildings.length > 0  && this.maximized && !this.isLoading && !this.searching;
    }
  },
  created(){
    let _vm = this;
    this.$root.$on('custom-analysis-close', () => {
      _vm.cancelDraw();
    });
    this.$root.$on('analysis-data-loading', loading => {
      this.loading = loading;
    })
    this.$root.$on('searching', val => {
      _vm.searching = val;
    });
  }
}
</script>
<style>
#draw {
  width: auto;
  left: 10px;
  z-index: 500;
}
#bbox-draw, #cancel-draw {
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  margin-left: .5em;
}
.loading {
  pointer-events: none;
  color: grey;

}
#title {
  font-size: 1em;
  font-weight: 600;
  width: auto;
}
#title.drawing {
  color: red;
}
</style>
