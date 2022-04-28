<template>
  <b-row no-gutters v-if="bins.length" class="pt-1">
    <b-col class="col-sm-7">
      <span id="height-filter">
        <b-icon-info-circle-fill font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      </span>
      <b-popover target="height-filter" triggers="hover" placement="auto">
        <template v-slot:title>
          <div>Height</div>
        </template>
        <template v-slot:default>
          <div>Filter buildings by height.</div>
        </template>
      </b-popover>
      <span class="heading text-uppercase text-muted">Height:</span>
    </b-col>
    <b-col sm="5">
      <vue-slider
        id="height-slider"
        v-model="buildingHeight" :min="minHeight" :max="maxHeight"
       @change="setHeightFilter($event)"
       :tooltip-formatter="tooltipFormatter"
      >
      </vue-slider>
    </b-col>
  </b-row>
</template>
<script>
export default {
  props: ['result'],
  data(){
    return {
      minHeight: 0,
      buildingHeight: this.minHeight,
      tooltipFormatter: "> {value} m",
      bins: this.result.buildings.height_bins,
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      }
    }
  },
  computed: {
    maxHeight(){
      return parseInt(this.result.buildings.max_height);
    },
    heightFilter(){
      return this.$store.getters['filters/getHeightFilter'];
    }
  },
  watch: {
    result(){
      if(this.heightFilter){
        this.buildingHeight = this.heightFilter[2];
      }
      else {
         this.buildingHeight = 0
      }
      this.setHeightFilter(this.buildingHeight);
    }
  },
  methods: {
    setHeightFilter(height){
      let height_filter = null;
      if(height >= this.minHeight && height <= this.maxHeight){
        height_filter = [">=", ["get", "d_avg_height"], height];
      }
      this.$store.commit('filters/setHeightFilter', height_filter);
      this.$emit('update:height', height);
    }
  },
  created(){
    let _vm = this;
    _vm.$root.$on('reset-filters',() => {
      _vm.buildingHeight = 0;
    });
  }
}
</script>
<style scoped>
#height-slider {
  margin-left: .5em;
  margin-right: 1.4em;
}
.heading {
  font-size: .7em;
}
</style>
