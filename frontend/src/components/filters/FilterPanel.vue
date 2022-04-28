<template>
  <div class="mb-5">
    <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.analysis>Analysis
      <span class="opened float-right"><b-icon-chevron-up font-scale="1.1"/></span>
      <span class="closed float-right"><b-icon-chevron-down font-scale="1.1"/></span>
    </div>
    <b-collapse id="analysis">
      <!-- <total-selected :map="map"></total-selected> -->
      <b-form-group class="mb-0">
        <b-form-checkbox-group id="prop-filter-group" v-model="selectedPropertyFilters" @input="runFilters()">
          <div v-for="(propFilter, propIdx)  in propertyFilters" :key="propIdx">
            <property-filter
              :id="'prop-filter-' + propIdx"
              :propFilter="propFilter"
              :result="result"
              :checked="selectedPropertyFilters"
              :indent="false">
            </property-filter>
          </div>
        </b-form-checkbox-group>
      </b-form-group>
      <b-form-group class="mt-2 mb-0">
        <b-row no-gutters>
          <b-col sm="7">
             <div class="filter-group-title"><small class="text-uppercase">Total Quality:</small></div>
          </b-col>
          <b-col sm="5">
            <b-checkbox @change="selectAllQuality($event)" :disabled="selectedUseFilters.length > 0"></b-checkbox>
          </b-col>
        </b-row>
        <b-form-checkbox-group id="quality-filter-group" v-model="selectedQualityFilters" @input="runFilters()">
          <div v-for="(qualityFilter, qualIdx) in qualityFilters" :key="qualIdx">
            <quality-filter
              :id="'quality-filter-' + qualIdx"
              :qualityFilter="qualityFilter"
              :result="result"
              :map="map"
              :checked="selectedQualityFilters">
            </quality-filter>
          </div>
        </b-form-checkbox-group>
      </b-form-group>
      <b-form-group class="mt-2 mb-2">
        <b-row no-gutters>
          <b-col sm="7">
             <div class="filter-group-title"><small class="text-uppercase">Use:</small></div>
          </b-col>
          <b-col sm="5">
            <b-checkbox @change="selectAllUse($event)" :disabled="selectedQualityFilters.length > 0"></b-checkbox>
          </b-col>
        </b-row>
        <b-form-checkbox-group id="use-filter-group" v-model="selectedUseFilters" @input="runFilters()">
          <div v-for="(useFilter, useIdx) in useFilters" :key="useIdx">
            <use-filter
              :id="'use-filter-' + useIdx"
              :useFilter="useFilter"
              :result="result"
              :checked="selectedUseFilters">
            </use-filter>
          </div>
        </b-form-checkbox-group>
      </b-form-group>
      <area-filter :result="result" @update:area="runFilters()"></area-filter>
      <height-filter :result="result" @update:height="runFilters()"></height-filter>
      <template v-if="displayTaxes">
        <tax-filter :result="result" @update:tax="runFilters()"></tax-filter>
        <tax-owed-filter :result="result" @update:tax-owed="runFilters()"></tax-owed-filter>
      </template>
    </b-collapse>
    <template v-if="displayCovid">
      <div class="hr w-100"></div>
      <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.covid>COVID-19
        <span class="opened float-right"><b-icon-chevron-up font-scale="1.1"/></span>
        <span class="closed float-right"><b-icon-chevron-down font-scale="1.1"/></span>
      </div>
      <b-collapse id="covid">
        <k3-filter :result="result" @update:covid="runFilters()"></k3-filter>
      </b-collapse>
    </template>
    <template v-if="displaySurvey">
      <div class="hr w-100"></div>
      <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.survey>Survey Analysis
        <span class="opened float-right"><b-icon-chevron-up font-scale="1.1"/></span>
        <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
      </div>
      <b-collapse id="survey">
        <b-form-checkbox-group id="survey-filter-group" v-model="selectedSurveyFilters" @input="runFilters()">
          <div v-for="(surveyProp, idx)  in surveyFilters" :key="idx">
            <survey-filter
              :id="'survey-prop-' + idx"
              :level="level"
              :result="result"
              :surveyProp="surveyProp"
              :checked="selectedSurveyFilters">
            </survey-filter>
          </div>
        </b-form-checkbox-group>
      </b-collapse>
    </template>
    <div class="hr w-100"></div>
    <span id="reset" class="float-right" @click="clearFilters()">Reset all filters</span>
  </div>
</template>
<script>
import { runFilter, resetFilters, runSpatialFilter } from "@/components/filters"
import { resetLayer, resetBuildings } from "@/components/map";
import { mapGetters } from 'vuex'
import PropertyFilter from "@/components/filters/PropertyFilter";
import QualityFilter from "@/components/filters/QualityFilter";
import UseFilter from "@/components/filters/UseFilter";
import SurveyFilter from "@/components/filters/SurveyFilter";
import AreaFilter from "@/components/filters/AreaFilter"
import HeightFilter from "@/components/filters/HeightFilter"
import TaxFilter from "@/components/filters/TaxFilter"
import TaxOwedFilter  from "@/components/filters/TaxOwedFilter";
import TotalSelected from "@/components/filters/TotalSelected";
import { TaxMixin } from "@/components/mixins/TaxesMixin"
import { K3Mixin } from "@/components/mixins/K3Mixin";
import K3Filter from "@/components/filters/K3Filter";
import { SurveyMixin } from "@/components/mixins/SurveyMixin";
import { InfrastructureMixin } from "@/components/mixins/InfrastructureMixin";
export default {
  mixins: [TaxMixin, K3Mixin, SurveyMixin, InfrastructureMixin],
  props: ['map','result', "level"],
  components: {
    PropertyFilter,
    QualityFilter,
    UseFilter,
    AreaFilter,
    HeightFilter,
    TaxFilter,
    TaxOwedFilter,
    K3Filter,
    SurveyFilter,
    TotalSelected,
  },
  computed: {
    ...mapGetters({
      propertyFilters: 'filters/getPropertyFilters',
      qualityFilters: 'filters/getQualityFilters',
      surveyFilters: 'filters/getSurveyFilters',
      selectedFeature: "maps/getSelectedFeature",
    }),
    selectedPropertyFilters: {
      get() {
        return this.$store.state.filters.selectedPropertyFilters;
      },
      set(filters){
        this.$store.commit('filters/setSelectedPropertyFilters', filters);
      }
    },
    selectedQualityFilters: {
      get(){
        return this.$store.state.filters.selectedQualityFilters;
      },
      set(filters){
        this.$store.commit("filters/setSelectedQualityFilters", filters);
      }
    },
    selectedUseFilters: {
      get(){
        return this.$store.state.filters.selectedUseFilters;
      },
      set(filters){
        this.$store.commit("filters/setSelectedUseFilters", filters);
      }
    },
    selectedSurveyFilters: {
      get() {
        return this.$store.state.filters.selectedSurveyFilters;
      },
      set(filters) {
        this.$store.commit('filters/setSelectedSurveyFilters', filters);
      }
    },
  },
  watch: {
    selectedFeature() {
      this.runFilters();
    },
  },
  methods: {
    runFilters(){
      runFilter(this, this.level);
    },
    clearFilters(){
      this.$store.dispatch("filters/clearFilters");
      this.$root.$emit('reset-filters');
      this.runFilters(this, this.level);
    },
    selectAllQuality(checked){
      this.selectedQualityFilters = checked ? this.qualityFilters : [];
    },
    selectAllUse(checked){
      this.selectedUseFilters = checked ? this.useFilters : [];
    }
  },
  created(){
    this.$root.$on('reset-map', () => {
      this.$store.dispatch("filters/clearFilters");
      this.$root.$emit('reset-filters');
      this.runFilters(this, 'aoi');
    });
  }
}
</script>
<style>
span.heading {
  font-size: .7em;
}
#reset {
  color: #C63D39;
  font-weight: 600;
  cursor: pointer;
  font-size: .9em;
  margin-bottom: 2rem;
}
.filter-group-title {
  /* font-size: .9em; */
  margin: .2em 0 .3em 0;
  font-weight: bolder !important;
}
</style>
