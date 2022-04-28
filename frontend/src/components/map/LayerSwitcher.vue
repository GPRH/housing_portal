<template>
  <div id="layer-switcher" v-if="maximized && show">
    <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.layers>
      <b-icon-layers-fill class="mr-2"></b-icon-layers-fill>Layers
      <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
      <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
    </div>
    <b-collapse id="layers" visible class="pb-2">
      <div v-for="(layer, idx) in layers" :key="idx" class="">
        <b-form-checkbox
          class="switcher ml-1"
          size="sm"
          :name="layer.id"
          :checked="layer.checked"
          :value="true"
          switch
          @change="toggleLayer($event, layer)"
        >
          <div class="d-flex legend-label">
            <app-legend class="mr-2 legend" :legend="getLegend(layer)"></app-legend>
            <span class="switcher-label font-weight-bolder">{{ layer.name }}</span>
          </div>
        </b-form-checkbox>
      </div>
    </b-collapse>
  </div>
</template>
<script>
import * as _ from "lodash";
import Legend from "@/components/map/Legend";
export default {
  props: ["layers", "map", "maximized", "show"],
  computed: {
    legends(){
      return this.$store.getters["maps/getLegends"];
    }
  },
  components: {
    appLegend: Legend
  },
  methods: {
    toggleLayer(checked, layer) {
      layer.checked = checked;
      if (checked) {
        this.showLayer(layer);
      } else {
        this.hideLayer(layer);
      }
    },
    showLayer(layer){
      this.map.setLayoutProperty(layer.id, "visibility", "visible");
      if(layer.id === 'buildings'){
        this.map.setLayoutProperty("building-outlines", "visibility", "visible");
      }
      if(layer.id === 'sectors'){
        this.map.setLayoutProperty('sector-outlines', 'visibility', 'visible');
      }
      if(layer.id === 'aoi'){
        this.map.setLayoutProperty("aoi-outline", "visibility", "visible");
      }
      if(layer.id === 'mapillary-images'){
        this.map.setLayoutProperty("mapillary-sequences", "visibility", "visible");
      }
    },
    hideLayer(layer){
      this.map.setLayoutProperty(layer.id, "visibility", "none");
      if(layer.id === 'buildings'){
        this.map.setLayoutProperty("building-outlines", "visibility", "none");
      }
      if(layer.id === 'sectors'){
        this.map.setLayoutProperty('sector-outlines', 'visibility', 'none');
      }
      if(layer.id === 'aoi'){
        this.map.setLayoutProperty("aoi-outline", "visibility", "none");
      }
      if(layer.id === 'mapillary-images'){
        this.map.setLayoutProperty("mapillary-sequences", "visibility", "none");
      }
    },
    getLegend(layer){
      return this.legends[layer.id];
    }
  }
};
</script>
<style scoped>
.collapsed > .open,
:not(.collapsed) > .closed {
  display: none;
}
#layer-switcher {
  color: black;
  background-color: transparent;
  font-family: 'Roboto Regular', sans-serif;
  pointer-events: all;
  /* border-top: 2px lightgrey solid; */
}
@media (max-width: 768px){
  #layer-switcher {
    bottom: 230px;
    width: 200px;
  }
}
.custom-switch, .switcher, .switcher-label, .legend {
  cursor: pointer !important;
}
.switcher-label {
  font-family: "Roboto Regular", sans-serif;
}
.fiscal {
  background-color: green;
  opacity: 0.5;
}
.privado {
  background-color: red;
  opacity: 0.5;
}
.legend-label {
  padding-top: .1rem;
}
</style>
