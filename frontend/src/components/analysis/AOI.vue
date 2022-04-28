<template>
  <div class="passport">
    <slot name="header"></slot>
    <b-collapse id="analysis-panel" visible>
        <div id="attrs" class="pt-2 pl-1 pr-1">
          <div role="button" class="section pt-1 text-uppercase text-dark font-weight-bold w-100" v-b-toggle.attributes>
            Attributes
            <span class="opened float-right"><b-icon-chevron-up font-scale="1.1"/></span>
            <span class="closed float-right"><b-icon-chevron-down font-scale="1.1"/></span>
          </div>
          <b-collapse id="attributes" visible>
            <dl class="row p-0">
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Name</small>
              </dt>
              <dd class="value col-sm-7">{{ selectedFeature.properties.name }}</dd>
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>size</small>
              </dt>
              <dd class="value col-sm-7">{{ result.area }} km<sup>2</sup></dd>
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>sectors</small>
              </dt>
              <dd class="value col-sm-7">{{ result.sectors }}</dd>
              <!-- <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>blocks (total)</small>
              </dt>
              <dd class="value col-sm-7">{{ result.blocks }}</dd> -->
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Buildings</small>
              </dt>
              <dd class="value col-sm-7">{{ formatNumber(result.buildings.count) }}</dd>
              <!-- <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Buildings (quality)</small>
              </dt>
              <dd class="value col-sm-7 tot-qualit">
                <svg width="22" height="22">
                  <circle fill="#fa0000" cx="10" cy="10" r="8"></circle>
                </svg>
                {{ result.buildings.very_poor }} % very poor
                <br/>
                <svg width="22" height="22">
                  <circle fill="#f26521" cx="10" cy="10" r="8"></circle>
                </svg>
                {{ result.buildings.poor }} % poor
                <br/>
                <svg width="22" height="22">
                  <circle fill="#f7941c" cx="10" cy="10" r="8"></circle>
                </svg>
                {{ result.buildings.fair }} % fair
                <br/>
                <svg width="22" height="22">
                  <circle fill="#91a23d" cx="10" cy="10" r="8"></circle>
                </svg>
                {{ result.buildings.good }} % good
                <br/>
                <svg width="22" height="22">
                  <circle fill="#008c50" cx="10" cy="10" r="8"></circle>
                </svg>
                {{ result.buildings.very_good }} % very good
              </dd> -->
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Roof area</small>
              </dt>
              <dd class="value col-sm-7">{{ result.buildings.avg_size }} m<sup>2</sup> (average)</dd>
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Building height</small>
              </dt>
              <dd class="value col-sm-6">{{ result.buildings.avg_height }} m (average)</dd>
              <!-- <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Residential</small>
              </dt>
              <dd class="value col-sm-6">{{ result.buildings.residential }} %</dd>
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Non-Residential</small>
              </dt>
              <dd class="value col-sm-6">{{ result.buildings.commercial }} %</dd>
              <dt class="heading col-sm-5 text-uppercase text-muted">
                <small>Mixed use</small>
              </dt>
              <dd class="value col-sm-6">{{ result.buildings.mixed }} %</dd> -->
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
          <div class="hr w-100"></div>
          <app-filter :map="map" :result="result" :level="level" :selectedFeature="selectedFeature"></app-filter>
        </div>
    </b-collapse>
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
  props: ["selectedFeature", "map", "level"],
  mixins: [FormatMixin, TaxMixin],
  components: {
    appChart: Chart,
    appScroll: Scroll,
    appFilter: FilterPanel
  },
  computed: {
    ...mapGetters({
      result: "analysis/getAOIAnalysis"
    }),
    area() {
      return parseFloat(this.result.area / 1000000).toFixed(2);
    },
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
    }
  },
  methods: {
    close() {
      this.$emit("close");
    },
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
