<template>
  <div id="aside">
    <app-building
      v-if="selectedFeature !== null && level === 'buildings'"
      :selectedFeature="selectedFeature"
    >
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            Building Passport
          </template>
        </app-header>
      </template>
    </app-building>
    <app-custom
      v-if="customAnalysis !== null"
      :result="customAnalysis"
      :map="map"
      :level="'custom'"
    >
      <template v-slot:header>
        <app-header @close="closeCustom()">
          <template v-slot:title>
            Custom Area statistics
          </template>
        </app-header>
      </template>
    </app-custom>
    <app-sector
      v-if="selectedFeature !== null && sectorAnalysis !== null && level === 'sectors'"
      :selectedFeature="selectedFeature"
      :result="sectorAnalysis"
      :map="map"
      :level="level"
    >
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            Sector Passport
          </template>
        </app-header>
      </template>
    </app-sector>
    <app-block
      v-if="selectedFeature !== null && blockAnalysis !== null && level === 'blocks'"
      :selectedFeature="selectedFeature"
      :result="blockAnalysis"
      :map="map"
      :level="level"
    >
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            Block Passport
          </template>
        </app-header>
      </template>
    </app-block>
    <app-plot
      v-if="selectedFeature !== null && level === 'plots'"
      :selectedFeature="selectedFeature"
    ></app-plot>
    <app-aoi
      v-if="selectedFeature !== null && aoiAnalysis !== null && level === 'aoi'"
      :selectedFeature="selectedFeature"
      :map="map"
      :level="level"
    >
      <template v-slot:header>
        <app-header @close="close()">
          <template v-slot:title>
            AOI Passport
          </template>
        </app-header>
      </template>
    </app-aoi>
    <app-info-footer
      v-if="showInfoFooter"
      @passport-info-click="infoClick()">
    </app-info-footer>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import Header from "@/components/analysis/Header";
import Building from "@/components/analysis/Building";
import Sector from "@/components/analysis/Sector";
import Block from "@/components/analysis/Block";
import Plot from "@/components/analysis/Plot";
import Aoi from "@/components/analysis/AOI";
import Custom from "@/components/analysis/Custom";
import InfoFooter from "@/components/info/InfoFooter"
import { resetLayers, resetBuildings } from "@/components/map"
import { runFilter, resetFilters } from "@/components/filters"
export default {
  props: ["map"],
  computed: {
    ...mapGetters({
      feature: "maps/getSelectedFeature",
      blockAnalysis: "analysis/getBlockAnalysis",
      sectorAnalysis: "analysis/getSectorAnalysis",
      aoiAnalysis: "analysis/getAOIAnalysis",
      customAnalysis: "analysis/getCustomAnalysis",
      layers: "maps/getLayers",
    }),
    selectedFeature() {
      if (this.feature !== null) {
        return this.feature.feature;
      }
      return null;
    },
    level() {
      if (this.feature !== null) {
        return this.feature.layer;
      }
      else if(this.customAnalysis !== null){
        return 'custom';
      }
    },
    showInfoFooter() {
      return (this.selectedFeature === null && this.level === 'custom')
      || (this.selectedFeature !== null && ["aoi", "sectors", "buildings"].includes(this.level));
    },
    isPozon() {
      return this.$store.getters["maps/getSelectedAoi"].name === "El Pozon";
    }
  },
  components: {
    appHeader: Header,
    appBuilding: Building,
    appSector: Sector,
    appAoi: Aoi,
    appBlock: Block,
    appPlot: Plot,
    appCustom: Custom,
    appInfoFooter: InfoFooter
  },
  methods: {
    close() {
      this.$store.dispatch("maps/clearSelectedFeature", { vm: this });
      resetLayers(this);
      this.clearFilters();
      resetBuildings(this);
      this.$root.$emit('analysis-close');
    },
    closeCustom(){
      this.close();
      this.$root.$emit('custom-analysis-close');
    },
    clearFilters(){
      this.map.setFilter("buildings", null);
      this.map.setFilter("building-outlines", null);
      this.$store.dispatch("filters/clearFilters");
    },
    infoClick(){
      this.$root.$emit('info-open', this.level);
    }
  },
};
</script>
<style>
#aside {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 500;
  pointer-events: all;
  height: auto;
}
@media (max-width: 768px){
  #aside {
    top: 60px;
  }
}
@media (max-width: 425px){
  #aside {
    top: 100px;
    width: 80vw;
  }
}
#footer {
  height: 1.5em;
  border-radius: 0px 0px 8px 8px;
}
.section {
  margin-bottom: 1em;
  font-size: .9em;
}
dt.heading {
  font-size: .9em;
}
dd.value {
  font-size: .9em;
  font-weight: 600;
}
.hr {
  border-top: 1px solid lightgrey;
  margin: 1em 0em 1em 0em;
}
.passport {
  border-radius: 0px 0px 8px 8px;
  line-height: 1.1rem;
  margin-bottom: 2rem;
}
</style>
