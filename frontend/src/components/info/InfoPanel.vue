<template>
  <div id="info-panel">
    <aoi-info :show="aoiAnalysis !== null && level === 'aoi'" @close="close()">
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            <b-icon-info-circle-fill class="info-icon"></b-icon-info-circle-fill>
            AOI Passport Information
          </template>
        </app-header>
      </template>
    </aoi-info>
    <sector-info :show="sectorAnalysis !== null && level === 'sectors'" @close="close()">
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            <b-icon-info-circle-fill class="info-icon"></b-icon-info-circle-fill>
            Sector Passport Information
          </template>
        </app-header>
      </template>
    </sector-info>
    <custom-info :show="customAnalysis !== null && level === 'custom'" @close="close()">
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            <b-icon-info-circle-fill class="info-icon"></b-icon-info-circle-fill>
            Custom Area Passport Information
          </template>
        </app-header>
      </template>
    </custom-info>
    <building-info :show="level === 'buildings'" @close="close()">
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            <b-icon-info-circle-fill class="info-icon"></b-icon-info-circle-fill>
            Building Passport Information
          </template>
        </app-header>
      </template>
    </building-info>
    <div class="footer"></div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import AOIInfo from "./AOIInfo";
import SectorInfo from "./SectorInfo";
import CustomInfo from "./CustomInfo";
import BuildingInfo from "./BuildingInfo";
import Header from "./Header";
export default {
  data(){
    return{
      level: null
    }
  },
  computed: {
    ...mapGetters({
      blockAnalysis: "analysis/getBlockAnalysis",
      sectorAnalysis: "analysis/getSectorAnalysis",
      aoiAnalysis: "analysis/getAOIAnalysis",
      customAnalysis: "analysis/getCustomAnalysis",
      layers: "maps/getLayers"
    }),
  },
  components: {
    aoiInfo: AOIInfo,
    sectorInfo: SectorInfo,
    customInfo: CustomInfo,
    buildingInfo: BuildingInfo,
    appHeader: Header,
  },
  methods: {
    close(){
      this.level = null;
    }
  },
  created(){
    let _vm = this;
    this.$root.$on('info-open', level => {
      _vm.level = level;
    });
    this.$root.$on('analysis-close', () => {
      this.level = null;
    });
  }

}
</script>
<style scoped>
#info-panel {
  /* max-height: 65vh; */
  position: fixed;
  right: 0px;
  top: 42px;
  z-index: 500;
   -webkit-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  border: none;
}
.footer {
  height: 1em;
  border-radius: 0px;
  border: none;
  pointer-events: all;
  background-color: white;
}
.info-icon {
  font-size: 1em;
}
</style>
