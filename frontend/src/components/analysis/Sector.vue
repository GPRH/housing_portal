<template>
  <div class="passport">
   <slot name="header"></slot>
   <!-- <app-scroll> -->
     <!-- <template v-slot:content> -->
       <b-collapse id="analysis-panel" visible>
          <div id="attrs" class="pt-2 pl-1 pr-1">
            <div class="section pt-1 text-uppercase text-dark font-weight-bold w-100" v-b-toggle.attributes>
              Attributes
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="attributes" visible>
              <dl class="row">
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Name</small>
                </dt>
                <dd class="value col-sm-7">{{ capitalize(selectedFeature.properties.name) }}</dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>size</small>
                </dt>
                <dd class="value col-sm-7">{{ result.area }} km<sup>2</sup></dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Buildings (total)</small>
                </dt>
                <dd class="value col-sm-7">{{ formatNumber(result.buildings.count) }}</dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Roof area</small>
                </dt>
                <dd class="value col-sm-7">{{ result.buildings.avg_size }} m<sup>2</sup> (average)</dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Building height</small>
                </dt>
                <dd class="value col-sm-6">{{ result.buildings.mixed }} %</dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Greenspace</small>
                </dt>
                <dd class="value col-sm-6">
                  <span v-html="formatGreenspace(result.greenspace.total_area)"></span>
                  ({{ result.greenspace.per_sec_area }} %)
                </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Roads</small>
                </dt>
                <dd class="value col-sm-6">Paved {{ result.roads.paved_length }} km; Unpaved {{ result.roads.unpaved_length }} km</dd>
                <template v-if="displayTaxes">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Average tax</small>
                  </dt>
                  <dd class="value col-sm-6">S/ {{ formatFloat(averageTaxes) }}</dd>
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Average tax owed</small>
                  </dt>
                  <dd class="value col-sm-6">S/ {{ formatFloat(averageTaxesOwed) }}</dd>
                </template>
              </dl>
            </b-collapse>
            <template v-if="result.buildings.count">
              <div class="hr w-100"></div>
              <app-filter :map="map" :result="result" :level="level" :selectedFeature="selectedFeature"></app-filter>
            </template>
          </div>
      </b-collapse>
     <!-- </template> -->
   <!-- </app-scroll> -->
  </div>
</template>
<script>
import numeral from "numeral";
import { mapGetters } from "vuex";
import Chart from "@/components/charts/Pie";
import Scroll from "@/components/analysis/Scroll"
import FilterPanel from "@/components/filters/FilterPanel"
import { FormatMixin } from "@/components/mixins/FormatMixin";
import { TaxMixin } from "@/components/mixins/TaxesMixin";
export default {
  props: ["selectedFeature", "result", "map", "level"],
  mixins: [FormatMixin, TaxMixin],
  components: {
    appChart: Chart,
    appScroll: Scroll,
    appFilter: FilterPanel
  },
  computed: {
    // area() {
    //   return parseFloat(this.result.sectorArea / 1000000).toFixed(2);
    // },
    heightChartData() {
      let lval = (this.result.countHeight / this.result.buildingCount) * 100;
      let fval = Math.round((100 - lval) * 100) / 100;
      return {
        labels: ["Buildings > 3.5m", "Buildings < 3.5m"],
        datasets: [
          {
            backgroundColor: ["#C12E3D", "#2E86C1"],
            data: [lval, fval]
          }
        ]
      };
    },
    roadChartData() {
      let lval = (this.result.unpavedCount / this.result.roadsCount) * 100;
      let fval = Math.round((100 - lval) * 100) / 100;
      return {
        labels: ["Unpaved Roads", "Paved roads"],
        datasets: [
          {
            backgroundColor: ["#C12E3D", "#2E86C1"],
            data: [lval, fval]
          }
        ]
      };
    }
  },
  methods: {
    displayChart() {
      return this.result.buildingCount > 0;
    },
    close() {
      this.$emit("close");
    }
  }
};
</script>
<style scoped>
.chart {
  width: 75%;
}
.tot-qualit > small {
  font-family: 'Roboto Medium', sans-serif;
}
</style>
