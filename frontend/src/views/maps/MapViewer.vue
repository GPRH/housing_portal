<template>
  <div>
    <b-container id="map-nav" class="p-0">
      <b-row no-gutters class="w-100">
        <b-col>
          <app-nav-bar @aoi-selected="selectAoi()" @show-downloads="showDownloads = true"></app-nav-bar>
        </b-col>
      </b-row>
    </b-container>
    <b-container id="map-viewport" class="p-0" fluid>
      <b-row no-gutters class="h-100 w-100">
        <b-col>
          <app-map :map="map" :maximized="!mlyMaximized"></app-map>
          <app-mapillary :map="map"></app-mapillary>
          <app-sidebar :map="map"></app-sidebar>
          <app-zoom-indicator :map="map"></app-zoom-indicator>
        </b-col>
      </b-row>
    </b-container>
    <b-container id="controls" class="p-0 h-100 w-100" fluid>
      <b-row no-gutters>
        <b-col cols="1"></b-col>
        <b-col cols="10">
          <app-info-panel></app-info-panel>
          <app-hover-info :map="map"></app-hover-info>
          <app-downloads :show="showDownloads" @dismissed="showDownloads = false"></app-downloads>
        </b-col>
        <b-col cols="1">
          <app-reset-view :map="map" :maximized="!mlyMaximized"></app-reset-view>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import {
  initMap,
  addControls,
  loadAOILayers,
  addEventHandlers,
} from "@/components/map";
import { selectSector, selectAoi, selectBuilding } from "@/components/map/events";
import { switchMapillaryAoi } from "@/components/mapillary";
import Navbar from "@/containers/Navbar.vue";
import { mapGetters } from "vuex";
import Draw from "@/components/draw/Draw";
import LayerSwitcher from "@/components/map/LayerSwitcher";
import Sidebar from "@/components/map/Sidebar";
import Map from "@/components/map/Map";
import Mapillary from "@/components/mapillary/Mapillary";
import { initMapillary } from "@/components/mapillary"
import Downloads from "@/components/downloads/Downloads";
import ZoomIndicator from "@/components/map/ZoomIndicator";
import Search from "@/components/map/Search";
import ResetView from "@/components/map/ResetView";
import HoverInfo from "@/components/map/HoverInfo";
import InfoPanel from "@/components/info/InfoPanel";
export default {
  name: "Map",
  props: ["aoiSlug", "geohash"],
  data() {
    return {
      map: null,
      mly: null,
      showAnalysis: false,
      mlyMaximized: false,
      showMapillary: false,
      showDownloads: false,
      isDrawing: false,
      isSwitching: false,
      isInitialLoad: false,
      isReset: false,
    };
  },
  components: {
    appMap: Map,
    appMapillary: Mapillary,
    appLayerSwitcher: LayerSwitcher,
    appNavBar: Navbar,
    appDownloads: Downloads,
    appDraw: Draw,
    appZoomIndicator: ZoomIndicator,
    appSearch: Search,
    appResetView: ResetView,
    appInfoPanel: InfoPanel,
    appHoverInfo: HoverInfo,
    appSidebar: Sidebar,
  },
  computed: {
    ...mapGetters({
      layers: "maps/getDisplayLayers",
      aoi: "maps/getSelectedAoi",
      selectedFeature: "maps/getSelectedFeature",
      config: "maps/getConfig",
    }),
    showLayerSwitcher(){
      return this.layers.length > 0;
    }
  },
  methods: {
    async initializeMap() {
      let _vm = this;
      await initMap(this);
      addControls(this, this.map);
      this.map.on("load", async () => {
        _vm.$root.$emit("map-init", _vm.map);
        console.log('Map loaded...')
        if(_vm.aoi){
          _vm.selectAoi();
        }
      });
    },
    async selectAoi(){
      this.isSwitching = true;
      this.map.setMinZoom(1);
      await loadAOILayers(this);
      addEventHandlers(this);
      this.$root.$emit('aoi-selected');
      this.isSwitching = false;
    }
  },
  mounted() {
    this.initializeMap();
  },
  created() {
    let _vm = this;
    this.$root.$on("resize-map", ({ show }) => {
      _vm.$nextTick(() => {
        _vm.map.resize();
      });
    });
    _vm.$root.$on("toggle-mapillary", () => {
      _vm.mlyMaximized = !_vm.mlyMaximized;
      _vm.$nextTick(() => {
        _vm.map.resize();
      });
    });
    _vm.$root.$on("draw-started", () => {
      _vm.isDrawing = true;
    });
    _vm.$root.$on("draw-stopped", () => {
      _vm.isDrawing = false;
    });
    _vm.$root.$on("draw-cancelled", () => {
      _vm.isDrawing = false;
    });
  },
  beforeRouteLeave (to, from, next) {
    if(to.name === 'Logout'){
      this.$root.$emit('before-logout');
    }
    next();
  }
};
</script>
<style scoped>
body {
  margin: 0;
}
#map-nav {
  position: absolute;
  top:0;
  left: 0;
  z-index: 300;
  height: 45px;
}
#map-viewport {
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  z-index: 100;
}
#controls {
  position: absolute;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  z-index: 200;
  pointer-events: none;
}
.b-side {
  pointer-events: all;
}
</style>
