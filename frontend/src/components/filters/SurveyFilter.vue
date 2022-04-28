<template>
  <b-row no-gutters>
    <b-col sm="7" class="text-uppercase text-muted">
      <b-icon-info-circle-fill :id="surveyProp.id + '-icon'" font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
      <b-popover :target="surveyProp.id + '-icon'" icon='info-circle' triggers="hover" placement="auto">
        <template v-slot:title>
          <div v-html="surveyProp.title"></div>
        </template>
        <template v-slot:default>
          <div v-html="surveyProp.desc"></div>
        </template>
      </b-popover>
      <span class="heading pr-1">{{ surveyProp.title }}</span>
    </b-col>
    <b-col sm="5">
      <b-form-checkbox
        :id="id"
        :name="surveyProp.id"
        :value="surveyProp"
      >
        <span v-if="isChecked">
          <small class="pl-2">
            <!-- <strong>{{ surveyProp.count }} </strong> -->
            <span class="text-muted">({{ percent }}%)</span>
          </small>
        </span>
      </b-form-checkbox>
    </b-col>
  </b-row>
</template>
<script>
import { mapGetters } from 'vuex';
import { FormatMixin } from "@/components/mixins/FormatMixin";
import { getBuildingFilter } from "@/components/filters";
import * as _ from "lodash"
export default {
  props: ['id', 'result','surveyProp', 'checked', 'level'],
  mixins: [FormatMixin],
  data(){
    return {
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      },
      count: 0
    }
  },
  computed: {
    isChecked(){
      return this.checked.includes(this.surveyProp);
    },
    percent() {
      return ((this.surveyProp.count / this.result.buildings.count) * 100).toFixed(2);
    }
  },
}
</script>
<style scoped>

</style>
