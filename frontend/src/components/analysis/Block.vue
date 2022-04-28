<template>
  <div>
    <slot name="header"></slot>
    <b-collapse id="analysis-panel" visible>
      <app-scroll>
        <template v-slot:content>
          <div id="attrs" class="p-3">
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.attributes>
              Attributes
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="attributes" visible>
              <dl class="row">
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Neghborhood</small>
                </dt>
                <dd class="value col-sm-7">{{ result.sector }}</dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>block size</small>
                </dt>
                <dd class="value col-sm-7">{{ result.area }} m<sup>2</sup></dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Buildings (total)</small>
                </dt>
                <dd class="value col-sm-7">{{ formatNumber(result.buildings.count) }}</dd>
                <dd class="col-sm-5"></dd>
                <dd class="value col-sm-7">
                  <svg width="20" height="20">
                    <circle fill="red" cx="10" cy="10" r="8"></circle>
                  </svg>
                  <small><strong> {{ result.buildings.poor }} % in poor condition</strong></small>
                  <br/>
                  <svg width="20" height="20">
                    <circle fill="orange" cx="10" cy="10" r="8"></circle>
                  </svg>
                  <small><strong> {{ result.buildings.fair }} % in fair condition</strong></small>
                  <br/>
                  <svg width="20" height="20">
                    <circle fill="green" cx="10" cy="10" r="8"></circle>
                  </svg>
                  <small><strong> {{ result.buildings.good }} % in good condition</strong></small>
                </dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Buildings size</small>
                </dt>
                <dd class="value col-sm-7">{{ result.buildings.avg_size }} m<sup>2</sup> (average)</dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Building height</small>
                </dt>
                <dd class="value col-sm-6">{{ result.buildings.avg_height }} m (average)</dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Residential</small>
                </dt>
                <dd class="value col-sm-6">{{ result.buildings.residential }} %</dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Commercial</small>
                </dt>
                <dd class="value col-sm-6">{{ result.buildings.commercial }} %</dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Mixed use</small>
                </dt>
                <dd class="value col-sm-6">{{ result.buildings.mixed }} %</dd>
                <dt class="header col-sm-5 text-uppercase text-muted">
                  <small>Greenspace</small>
                </dt>
                <dd class="value col-sm-6">{{ result.greenspace.total_area }} m<sup>2</sup> ({{ result.greenspace.per_sec_area }} %)</dd>
              </dl>
            </b-collapse>
            <div class="hr w-100"></div>
            <app-filter :map="map" :result="result" :level="level" :selectedFeature="selectedFeature"></app-filter>
            <!-- <div class="chart mb-4" v-if="result.buildingCount > 0 && result.countHeight > 0">
              <app-chart :chart-data="heightChartData"></app-chart>
            </div> -->
          </div>
        </template>
      </app-scroll>
    </b-collapse>
  </div>
</template>
<script>
import { FormatMixin } from "@/components/mixins/FormatMixin";
import { mapGetters } from "vuex";
import Chart from "@/components/charts/Pie";
import Scroll from "@/components/analysis/Scroll"
import FilterPanel from "@/components/filters/FilterPanel"
export default {
  props: ["map", "result", "selectedFeature", "level"],
  mixins: [FormatMixin],
  components: {
    appChart: Chart,
    appScroll: Scroll,
    appFilter: FilterPanel
  },
  computed: {
    // heightChartData() {
    //   let lval = (this.result.countHeight / this.result.buildingCount) * 100;
    //   let fval = Math.round((100 - lval) * 100) / 100;
    //   return {
    //     labels: ["Buildings > 3.5m", "Buildings < 3.5m"],
    //     datasets: [
    //       {
    //         backgroundColor: ["#C12E3D", "#2E86C1"],
    //         data: [lval, fval]
    //       }
    //     ]
    //   };
    // }
  },
};
</script>
<style scoped>
.chart {
  width: 75%;
}
</style>
