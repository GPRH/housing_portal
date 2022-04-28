<template>
  <b-row no-gutters v-if="bins.length" class="pt-1">
    <b-col sm="7">
      <span id="tax-owed-filter-icon">
        <b-icon-info-circle-fill font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      </span>
      <b-popover target="tax-owed-filter-icon" triggers="hover" placement="auto">
        <template v-slot:title>
          <div>Average Tax Owed</div>
        </template>
        <template v-slot:default>
          <div>Filter buildings by average tax owed.</div>
        </template>
      </b-popover>
      <span class="heading text-uppercase text-muted">Average tax owed:</span>
    </b-col>
    <b-col sm="5">
      <vue-slider
        id="tax-owed-slider"
        v-model="value" :data="bins"
        :included="true" :marks="bins" :hide-label="true"
        :tooltip-formatter="tooltipFormatter"
        @change="setTaxFilter($event)"
      >
        <template v-slot:step="{ label, active }">
          <div :id="'tax-owed-step-' + label" :class="['custom-step', { active }]"></div>
          <b-tooltip placement="top" container="tax-owed-slider" custom-class="tax-tooltip" :target="'tax-owed-step-' + label" :title="'> S/ ' + formatNumber(label)"></b-tooltip>
       </template>
      </vue-slider>
    </b-col>
  </b-row>
</template>
<script>
import { FormatMixin } from "@/components/mixins/FormatMixin";
export default {
  props: ['result'],
  mixins: [FormatMixin],
  data(){
    return {
      value: 0,
      minTax: 0,
      bins: this.result.buildings.taxes.tax_owed_bins,
      tooltipFormatter: value => `S/ ${this.formatNumber(value)}`,
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      }
    }
  },
  computed: {
    taxFilter(){
      return this.$store.getters["filters/getTaxOwedFilter"];
    }
  },
  watch: {
    result(){
      if(this.taxFilter){
        this.value = this.taxFilter[2];
      }
      else {
        this.value = 0;
      }
      this.setTaxFilter(this.value);
    }
  },
  methods: {
    setTaxFilter(value){
      let tax_filter = null;
      if(value > this.minTax){
        tax_filter = [">=", ["get", "pt_avg_owed"], value];
      }
      this.$store.commit('filters/setTaxOwedFilter', tax_filter)
      this.$emit('update:tax-owed', value);
    }
  },
  created(){
    let _vm = this;
    _vm.$root.$on('reset-filters',() => {
      _vm.value = 0;
    });
  }
}
</script>
<style>
.custom-step {
  width: 100%;
  height: 100%;
  background-color: #3498db;
}
.custom-step:hover {
  cursor: pointer;
}
.custom-step.active {
  background-color: #3498db;
}
.tooltip-inner {
  background-color: #3498db !important;
}
.bs-tooltip-top .arrow::before, .bs-tooltip-auto[x-placement^="top"] .arrow::before {
    top: 0;
    border-width: 0.4rem 0.4rem 0;
    border-top-color: #3498db !important;
}
#tax-owed-slider {
  margin-left: .5em;
  margin-right: 1.4em;
}
.heading {
  font-size: .7em;
}
</style>
