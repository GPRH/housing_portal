<template>
  <div id="sidbar-wapper" v-show="aoi && showLayerSwitcher">
    <b-sidebar id="sidebar" no-header visible no-close-on-esc @shown="show()" @hidden="shown=false">
      <template v-slot:default>
        <app-scroll>
          <template v-slot:content>
            <div class="p-2">
              <app-search :map="map"></app-search>
            </div>
            <div class="p-2">
              <app-draw :map="map" :maximized="!mlyMaximized"></app-draw>
              <div class="mt-2 section-break mx-auto" v-if="!mlyMaximized && showPassport"></div>
            </div>
            <div class="p-2">
              <app-passport :map="map"></app-passport>
              <div class="mt-2 section-break mx-auto"></div>
            </div>
            <div class="p-2">
              <app-layer-switcher
                :map="map"
                :layers="layers"
                :maximized="!mlyMaximized"
                :show="showLayerSwitcher"
              ></app-layer-switcher>
              <!-- <div class="mt-2 section-break mx-auto" v-if="showLayerSwitcher && !mlyMaximized"></div> -->
            </div>
          </template>
        </app-scroll>
      </template>
    </b-sidebar>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import Search from "@/components/map/Search";
import LayerSwitcher from "@/components/map/LayerSwitcher";
import Draw from "@/components/draw/Draw";
import Map from "@/components/map/Map";
import AnalysisPanel from "@/components/analysis/AnalysisPanel";
import Scroll from "@/components/analysis/Scroll"
export default {
  props: ["map"],
  data(){
    return {
      shown: false,
      mlyMaximized: false,
    }
  },
  computed: {
    ...mapGetters({
      layers: "maps/getDisplayLayers",
      aoi: "maps/getSelectedAoi",
      selectedFeature: "maps/getSelectedFeature",
      customAnalysis: "analysis/getCustomAnalysis",
      config: "maps/getConfig",
    }),
    showLayerSwitcher(){
      return this.layers.length > 0;
    },
    showPassport() {
      return this.selectedFeature !== null || this.customAnalysis !== null;
    },
    aoi(){
      return this.$store.getters['maps/getSelectedAoi'];
    },
  },
  methods: {
    show(){
      this.shown = true;
    }
  },
  components: {
    appSearch: Search,
    appLayerSwitcher: LayerSwitcher,
    appDraw: Draw,
    appMap: Map,
    appPassport: AnalysisPanel,
    appScroll: Scroll
  },
  created(){
     let _vm = this;
    _vm.$root.$on("toggle-mapillary", () => {
      _vm.mlyMaximized = !_vm.mlyMaximized;
      _vm.$nextTick(() => {
        _vm.map.resize();
      });
    });
  }
}
</script>
<style>
#sidebar-wrapper {
  height: 0;
  background-color: red;
}
#sidebar {
  position: absolute;
  pointer-events: all;
  height: auto;
  top: 42px !important;
  background-color: white !important;
  font-family: "Roboto Regular", sans-serif;
  border-bottom-right-radius: 4px;
  z-index: 1202;
  width: 364px !important;
  padding: 0px 5px 0px 5px;
  overflow: hidden;
}
#sidebar-toggle {
  position:absolute;
  background-color: white;
  width: 40px;
  height: 40px;
  top: 58px;
  left: 0px;
  z-index: 1000;
  font-size: 1.5em;
  font-weight: 600;
  opacity: .95;
}
.b-sidebar-body {
  height: auto;
}
.b-sidebar-outer {
  height: 100% !important;
  pointer-events: none;
}
/* #sidebar-toggle:hover {
  color: grey;
} */
.ps {
  height: auto;
  max-height: calc(100vh - 43vh);
}
h5 {
  font-family: "Roboto Medium", sans-serif;
}
.close {
  cursor: pointer;
  font-size: 1.5em;
  font-weight: 600;
}
.close:hover {
  color: grey;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.section-break {
  padding-top: .2em;
  border-bottom: 1px solid lightgrey;
}
</style>
