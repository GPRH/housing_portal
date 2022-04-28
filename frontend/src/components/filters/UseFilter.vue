<template>
  <b-row no-gutters>
    <b-col sm="7" class="text-uppercase text-muted indent">
      <b-icon-info-circle-fill :id="useFilter.id + '-icon'" font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      <b-popover :target="useFilter.id + '-icon'" icon='info-circle' triggers="hover" placement="auto">
        <template v-slot:title>
          <div v-html="useFilter.title"></div>
        </template>
        <template v-slot:default>
          <div v-html="useFilter.desc"></div>
        </template>
      </b-popover>
      <span id="prop-title" class="heading pr-1">{{ useFilter.title }}</span>
    </b-col>
    <b-col sm="5">
      <b-form-checkbox
        :id="id"
        :name="useFilter.id"
        :value="useFilter"
        :disabled="disabled"
        class="align-top"
      >
        <span v-show="active" class="legend">
          <svg width="16px" height="16px">
            <rect :fill="useFilter.color" width="16px" height="16px"></rect>
          </svg>
          <!-- <svg width="15" height="15">
            <circle :fill="useFilter.color" cx="7.5" cy="7.5" r="7"></circle>
          </svg>
          <span class="result-count pl-1">{{ formatNumber(result.buildings[useFilter.resultProp]) }}</span> -->
          <span class="result-percent pl-1" v-if="useFilter.percentProp">
            {{ result.buildings[useFilter.percentProp] }}%
          </span>
        </span>
      </b-form-checkbox>
    </b-col>
  </b-row>
</template>
<script>
import { mapGetters } from 'vuex'
import { FormatMixin } from "@/components/mixins/FormatMixin";
import * as _ from "lodash"
export default {
  props: ['id', 'useFilter', 'result', 'checked'],
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
      qualityFilters: 'filters/getSelectedQualityFilters',
    }),
    active() {
      return this.checked.includes(this.useFilter);
    },
    disabled() {
      return this.qualityFilters.length > 0;
    }
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
