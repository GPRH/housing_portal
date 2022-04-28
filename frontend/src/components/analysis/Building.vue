<template>
  <div v-if="selectedFeature">
    <slot name="header"></slot>
    <b-collapse id="analysis-panel" visible>
      <!-- <app-scroll>
        <template v-slot:content> -->
          <div id="attrs" class="pt-2 pl-1 pr-1">
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.images>
              Image
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="images" class="pb-2">
              <div v-if="images.length">
                <b-img :src="images[0].url" fluid rounded width="350" height="350"></b-img>
              </div>
              <div v-else>No images found.</div>
            </b-collapse>
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.location>
              Location
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="location">
              <dl class="row">
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>City</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.city">
                  {{ properties.city }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Area of Interest</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.aoi_name">
                  {{ properties.aoi_name }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Sector</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.sector_name">
                  {{ properties.sector_name }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Address</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.address">
                  {{ properties.address }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Coordinates</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.center">
                  {{ properties.center[1] }}, {{ properties.center[0] }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-5 text-uppercase text-muted">
                  <small>Geohash</small>
                </dt>
                <dd class="value col-sm-7" v-if="properties.geohash">
                  {{ properties.geohash }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
              </dl>
            </b-collapse>
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.attributes>Attributes
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="attributes">
              <dl class="row">
                <template v-if="displayAttr('d_material')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Roof material</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_material">
                    <app-confidence
                      :id="'d-material-confidence'"
                      :attr="'d_' + properties.d_material"
                      :confidence_values="confidence_values"
                      :title="'Roof Material Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('d_condition')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Roof condition</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_condition">
                    <app-confidence
                      :id="'d--confidence'"
                      :attr="'d_' + properties.d_condition"
                      :confidence_values="confidence_values"
                      :title="'Roof Condition Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('d_avg_height')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Height</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_avg_height">
                    {{ formatFloat(properties.d_avg_height) }} m
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('d_slope')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Ground Slope</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_slope">
                    {{ formatFloat(properties.d_slope) }}&deg;
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('d_volume')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Volume</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_volume">
                    {{ formatFloat(properties.d_volume) }} m<sup>3</sup>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('d_area')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Area</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.d_area">
                    {{ formatFloat(properties.d_area) }} m<sup>2</sup>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayTaxes">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Average tax</small>
                  </dt>
                  <dd class="value col-sm-7">S/ {{ formatFloat(averageTax) }}</dd>
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Average tax owed</small>
                  </dt>
                  <dd class="value col-sm-7">S/ {{ formatFloat(averageTaxOwed) }}</dd>
                </template>
                <template v-if="displayAttr('sv_design')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Designed</small>
                  </dt>
                  <dd class="value col-sm-7 no-wrap" v-if="properties.sv_design">
                    <app-confidence
                      :id="'sv-design-confidence'"
                      :attr="properties.sv_design"
                      :confidence_values="confidence_values"
                      :title="'Design Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_materia')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Wall material</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_materia">
                    <app-confidence
                      :id="'sv-material-confidence'"
                      :attr="properties.sv_materia"
                      :confidence_values="confidence_values"
                      :title="'Wall Material Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_condit')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Wall condition</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_condit">
                    <app-confidence
                      :id="'sv-condition-confidence'"
                      :attr="properties.sv_condit"
                      :confidence_values="confidence_values"
                      :title="'Condition Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_use')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Use</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_use">
                    <app-confidence
                      :id="'sv-use-confidence'"
                      :attr="properties.sv_use"
                      :confidence_values="confidence_values"
                      :title="'Use Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_securit')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Security</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_securit">
                    <app-confidence
                      :id="'sv-securit-confidence'"
                      :attr="properties.sv_securit"
                      :confidence_values="confidence_values"
                      :title="'Security Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_contru')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Construction</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_constru">
                    <app-confidence
                      :id="'sv-constru-confidence'"
                      :attr="properties.sv_constru"
                      :confidence_values="confidence_values"
                      :title="'Construction Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_vintage')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Vintage</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_vintage && properties.sv_vintage !== '0'">
                    <app-confidence
                      :id="'sv-vintage-confidence'"
                      :attr="properties.sv_vintage"
                      :confidence_values="confidence_values"
                      :title="'Vintage Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('sv_complet')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Complete</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.sv_complet">
                    <app-confidence
                      :id="'sv-complet-confidence'"
                      :attr="properties.sv_complet"
                      :confidence_values="confidence_values"
                      :title="'Completness Confidence Value'">
                    </app-confidence>
                  </dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
                <template v-if="displayAttr('land_publi')">
                  <dt class="heading col-sm-5 text-uppercase text-muted">
                    <small>Public land</small>
                  </dt>
                  <dd class="value col-sm-7" v-if="properties.land_publi === 1">yes</dd>
                  <dd class="value col-sm-7" v-if="properties.land_publi === 0">no</dd>
                  <dd class="value col-sm-7" v-else> -- </dd>
                </template>
              </dl>
            </b-collapse>
            <!--
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.risks>Risks
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="risks">
              <dl class="row">
                <dt class="heading col-sm-6 text-uppercase text-muted">
                  <small>Disaster mitigation</small>
                </dt>
                <dd class="value col-sm-6" v-if="properties.sv_disaster === 1 || properties.sv_disaster === 0">
                  {{ properties.sv_disaster === 1 ? 'yes' : 'no' }}
                  <b-icon-info-circle-fill id="sv-disaster-info-icon" :style="iconStyle" font-scale=".9"></b-icon-info-circle-fill>
                  <b-popover target="sv-disaster-info-icon" triggers="hover" placement="top" title="Disaster confidence value">
                    {{ getConfidenceValue(properties.sv_disaster) }}
                  </b-popover>
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
              </dl>
            </b-collapse>
            -->
            <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.analysis>Analysis
              <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
              <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
            </div>
            <b-collapse id="analysis">
              <dl class="row">
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Resettlement</small>
                </dt>
                <dd class="value col-sm-5 text-lowercase" v-if="properties.dem_reset">
                    <!-- <svg width="20" height="20">
                      <circle :fill="properties.dem_reset === 'YES' ? 'green': 'red'" cx="10" cy="10" r="8"></circle>
                    </svg> -->
                  {{ properties.dem_reset }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Structural Improvement</small>
                </dt>
                <dd class="value col-sm-5 text-lowercase" v-if="properties.dem_struct">
                  <!-- <svg width="20" height="20">
                    <circle :fill="properties.dem_struct === 'YES' ? 'greem': 'red'" cx="10" cy="10" r="8"></circle>
                  </svg> -->
                 {{ properties.dem_struct }}
                </dd>
                <dd class="value col-sm-6" v-else> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Quality Improvement</small>
                </dt>
                <dd class="value col-sm-5 text-lowercase" v-if="properties.dem_qualit">
                  <!-- <svg width="20" height="20">
                    <circle :fill="properties.dem_qualit === 'YES' ? 'greem': 'red'" cx="10" cy="10" r="8"></circle>
                  </svg> -->
                  {{ properties.dem_qualit }}
                </dd>
                <dd class="value col-sm-5" v-else> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Expansion</small>
                </dt>
                <dd class="value col-sm-5 text-lowercase" v-if="properties.opp_expansion">
                  <!-- <svg width="20" height="20">
                    <circle :fill="properties.opp_expansion === 'YES' ? 'greem': 'red'" cx="10" cy="10" r="8"></circle>
                  </svg> -->
                  {{ properties.opp_expansion }}
                </dd>
                <dd class="value col-sm-5" v-else> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>payment capacity</small>
                </dt>
                <dd class="value col-sm-5"> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Home insurance</small>
                </dt>
                <dd class="value col-sm-5"> -- </dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Home microfinance</small>
                </dt>
                <dd class="value col-sm-5"> -- </dd>
                <!-- <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Structural & Quality Improvements</small>
                </dt>
                <dd class="value col-sm-5">
                  <svg width="20" height="20">
                    <circle :fill="selectedFeature.dem_struct === 'YES' ? 'greem': 'red'" cx="10" cy="10" r="8"></circle>
                  </svg>
                  <strong> {{ selectedFeature.dem_both }} </strong>
                </dd> -->
                <!-- <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Total Quality</small>
                </dt>
                <dd class="value col-sm-5">{{ selectedFeature.tot_qualit }}</dd> -->
                <!-- <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Soft Story</small>
                </dt>
                <dd class="value col-sm-5">{{ selectedFeature.soft_story }}</dd>
                <dt class="heading col-sm-7 text-uppercase text-muted">
                  <small>Value</small>
                </dt>
                <dd class="value col-sm-5">{{ selectedFeature.value }}</dd> -->
              </dl>
            </b-collapse>
            <template v-if="displayCovid">
              <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.covid>COVID-19
                <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
                <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
              </div>
              <b-collapse id="covid">
                <dl class="row">
                  <dt class="heading col-sm-7 text-uppercase text-muted">
                    <small>Covid Vulnerability Index</small>
                  </dt>
                  <dd class="value col-sm-5" v-if="properties.k3">
                    <svg width="20" height="20">
                      <circle :fill="getCovidDisplay(properties.k3)" cx="10" cy="10" r="8"></circle>
                    </svg>
                  <strong> {{ formatFloat(properties.k3)  }} </strong>
                  </dd>
                  <dd class="value col-sm-6" v-else> -- </dd>
                </dl>
              </b-collapse>
            </template>
            <template v-if="hasExtraAttrs">
              <div class="section text-uppercase text-dark font-weight-bold w-100" v-b-toggle.survey>Survey
                <span class="opened float-right"><b-icon-chevron-up font-scale="1.1" /></span>
                <span class="closed float-right"><b-icon-chevron-down font-scale="1.1" /></span>
              </div>
              <b-collapse id="survey">
                <app-attrs :attrs="properties.extra_attrs"></app-attrs>
              </b-collapse>
            </template>
          </div>
        <!-- </template>
      </app-scroll> -->
    </b-collapse>
  </div>
</template>
<script>
import { FormatMixin } from "@/components/mixins/FormatMixin";
import { TaxMixin } from "@/components/mixins/TaxesMixin";
import { K3Mixin } from "@/components/mixins/K3Mixin";
import { AttrMixin } from "@/components/mixins/AttrMixin";
import Scroll from "@/components/analysis/Scroll"
import ConfidenceLevel from "@/components/analysis/ConfidenceLevel";
import ExtraAttrs from "@/components/analysis/ExtraAttrs";
import * as _ from "lodash";
export default {
  props: ["selectedFeature"],
  mixins: [FormatMixin, TaxMixin, K3Mixin, AttrMixin],
  data(){
    return {
      iconStyle: {
        color: '#2E94C1',
        cursor: 'pointer',
        "font-size": '.9em'
      }
    }
  },
  components: {
    appScroll: Scroll,
    appConfidence: ConfidenceLevel,
    appAttrs: ExtraAttrs
  },
  methods: {
    close() {
      this.$emit("close");
    },
    getCovidDisplay(val){
      let value = val === null ? 0 : parseFloat(val);
      if(value <= 1.2){
        return 'red';
      }
      if(value <= 1.61 && value > 1.2){
        return 'orange'
      }
      else {
        return 'green'
      }
    }
  },
  computed: {
    properties() {
      return this.selectedFeature.properties;
    },
    aoi(){
      return this.$store.getters["maps/getSelectedAoi"];
    },
    images(){
      let images = [];
      for (let image of this.selectedFeature.properties.images){
        let img = {};
        let country = this.aoi.country.toLowerCase();
        let city = this.aoi.city.toLowerCase();
        img.url = `/api/geodata/images/${country}/${city}/${image.image_name}`;
        img.class = image.class_str;
        img.confidence = image.confidence;
        images.push(img);
      }
      return images;
    },
    confidence_values(){
      return this.selectedFeature.properties.confidence_values
    },
    averageTax(){
      return   this.properties.pt_sum / this.properties.count;
    },
    averageTaxOwed(){
      return this.properties.pt_sum_owed / this.properties.count;
    },
    hasExtraAttrs(){
      return this.properties.extra_attrs !== null;
    }
  }
};
</script>
<style>
.collapsed > .opened,
:not(.collapsed) > .closed {
  display: none;
}
.opened:hover, .closed:hover {
  cursor: pointer;
}
.section {
  color: #434343;
}
#building-images {
  border: 1px solid lightgrey;
  border-radius: 4px;
}
</style>
