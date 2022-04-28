<template>
  <b-row no-gutters v-if="bins.length">
    <b-col sm="7">
      <span id="area-filter"><b-icon-info-circle-fill font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill></span>
      <b-popover target="area-filter" triggers="hover" placement="auto">
        <template v-slot:title>
          <div>Area</div>
        </template>
        <template v-slot:default>
          <div>Filter buildings by area.</div>
        </template>
      </b-popover>
      <span class="heading text-uppercase text-muted">Area:</span>
    </b-col>
    <b-col sm="5">
      <vue-slider
        id="area-slider"
        v-model="buildingSize" :min="minSize" :data="bins" :included="true" :marks="bins" :hide-label="true"
       @change="setAreaFilter($event)" :tooltip-formatter="tooltipFormatter"
      >
        <template v-slot:step="{ label, active }">
          <div :id="'area-step-' + label" :class="['custom-step', { active }]"></div>
          <b-tooltip container="area-slider" custom-class="step-tooltip" :target="'area-step-' + label" :title="'> ' +  formatNumber(label)  + ' m2'"></b-tooltip>
       </template>
      </vue-slider>
    </b-col>
  </b-row>
</template>
<script>
import {FormatMixin} from "@/components/mixins/FormatMixin"
export default {
  props: ['result'],
  mixins: [FormatMixin],
  data(){
    return {
      minSize: 0,
      buildingSize: this.minSize,
      tooltipFormatter: value => `> ${this.formatNumber(value)} m2`,
      bins: this.result.buildings.size_bins,
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      }
    }
  },
  computed: {
    maxSize(){
      return parseInt(this.result.buildings.max_size);
    },
    areaFilter(){
      return this.$store.getters["filters/getAreaFilter"];
    }
  },
  watch: {
    result(){
      if(this.areaFilter){
        this.buildingSize = this.areaFilter[2];
      }
      else {
        this.buildingSize = 0;
      }
      this.setAreaFilter(this.buildingSize);
    }
  },
  methods: {
    setAreaFilter(size){
      let area_filter = null;
      if(size > this.minSize){
        area_filter = [">", ["get", "d_area"], size];
      }
      this.$store.commit('filters/setAreaFilter', area_filter)
      this.$emit('update:area', size);
    },
  },
  created(){
    let _vm = this;
    _vm.$root.$on('reset-filters',() => {
      _vm.buildingSize = 0;
    });
  }
}
</script>
<style scoped>
#area-slider {
  margin-left: .5em;
  margin-right: 1.4em;
}
.heading {
  font-size: .7em;
}
.custom-step {
  width: 100%;
  height: 100%;
  /* border-radius: 50%; */
  /* box-shadow: 0 0 0 2px #ccc; */
  background-color: #3498db;
}
.custom-step:hover {
  cursor: pointer;
}
.custom-step.active {
  /* box-shadow: 0 0 0 1px #3498db; */
  background-color: #3498db;
}
.step-tooltip {
  background-color: #3498db;
  font-size: .8em;
}
</style>
