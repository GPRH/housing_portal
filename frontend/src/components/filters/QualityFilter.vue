<template>
  <b-row no-gutters>
    <b-col sm="7" class="text-uppercase text-muted indent">
      <b-icon-info-circle-fill :id="qualityFilter.id + '-icon'" font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      <b-popover :target="qualityFilter.id + '-icon'" icon='info-circle' triggers="hover" placement="auto">
        <template v-slot:title>
          <div v-html="qualityFilter.title"></div>
        </template>
        <template v-slot:default>
          <div v-html="qualityFilter.desc"></div>
        </template>
      </b-popover>
      <span id="prop-title" class="heading pr-1">{{ qualityFilter.title }}</span>
    </b-col>
    <b-col sm="5">
      <b-form-checkbox
        :id="id"
        :name="qualityFilter.id"
        :value="qualityFilter"
        :disabled="disabled"
        class="align-middle"
      >
        <div v-show="active" class="legend">
          <svg width="16px" height="16px">
            <rect :fill="qualityFilter.color" width="16px" height="16px"></rect>
          </svg>
          <!-- <svg width="15" height="15">
            <circle :fill="qualityFilter.color" cx="7.5" cy="7.5" r="7"></circle>
          </svg> -->
          <!-- <span class="result-count pl-1">{{ formatNumber(result.buildings[qualityFilter.resultProp]) }}</span> -->
          <!-- <span>{{ total }}</span> -->
          <span class="result-percent pl-1" v-if="qualityFilter.percentProp">
            {{ result.buildings[qualityFilter.percentProp] }}%
          </span>
        </div>
      </b-form-checkbox>
    </b-col>
  </b-row>
</template>
<script>
import { mapGetters } from 'vuex'
import { FormatMixin } from "@/components/mixins/FormatMixin";
import * as _ from "lodash"
export default {
  props: ['id', 'qualityFilter', 'result', 'map', 'checked'],
  mixins: [FormatMixin],
  data(){
    return {
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      }
    }
  },
  computed: {
    ...mapGetters({
      filters: 'filters/getFilters',
      useFilters: 'filters/getSelectedUseFilters',
    }),
    active() {
      return this.checked.includes(this.qualityFilter);
    },
    disabled() {
      return this.useFilters.length > 0;
    },
    // total(){
    //   return this.map.querySourceFeatures(
    //     "buildings", {sourceLayer: 'default', filter: this.qualityFilter.expression}
    //   ).length
    // }
  }
}
</script>
<style scoped>
.result-count, .result-percent {
  font-size: .7em;
}
.indent {
  padding-left: 20px !important;
}
.legend {
  margin-top: 2px;
  cursor: pointer;
}
</style>
