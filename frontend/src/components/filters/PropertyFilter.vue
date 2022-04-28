<template>
  <b-row no-gutters>
    <b-col sm="7" class="text-uppercase text-muted" :class="{ indent: indent}">
      <b-icon-info-circle-fill :id="propFilter.id + '-icon'" font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      <b-popover :target="propFilter.id + '-icon'" icon='info-circle' triggers="hover" placement="auto">
        <template v-slot:title>
          <div v-html="propFilter.title"></div>
        </template>
        <template v-slot:default>
          <div v-html="propFilter.desc"></div>
        </template>
      </b-popover>
      <span class="heading pr-1">{{ propFilter.title }}</span>
    </b-col>
    <b-col sm="5">
      <b-form-checkbox
        :id="id"
        :name="propFilter.id"
        :value="propFilter"
        :disabled="disabled"
        class="align-middle"
      >
        <span v-show="active && displayLegend" class="legend">
          <!-- <svg width="15" height="15">
            <rect :fill="propFilter.color" width="14px" height="14px"></rect>
          </svg> -->
          <!-- <span class="result-count pl-1">{{ formatNumber(result.buildings[propFilter.resultProp]) }}</span> -->
          <span class="result-percent pl-1" v-if="propFilter.percentProp">
            {{ result.buildings[propFilter.percentProp] }}%
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
  props: ['id', 'propFilter', 'result', 'checked', 'indent'],
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
      useFilters: 'filters/getSelectedUseFilters',
    }),
    active() {
      return this.checked.includes(this.propFilter);
    },
    qualChecked() {
      return this.qualityFilters.length > 0;
    },
    useChecked() {
      return this.useFilters.length > 0;
    },
    disabled() {
      let disabled = false;
      // no filters applied - all enabled
      if(!this.checked.length) {
        disabled = false;
      }
      return disabled;
    },
    displayLegend(){
      return !this.useChecked && !this.qualChecked;
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
