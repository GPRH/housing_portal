<template>
  <div>
    <span>{{ attribute }} &nbsp;</span>
    <template v-if="wrapStars">
      <br/>
    </template>
    <b-popover :target="id" triggers="hover" placement="top">
      <span class="p-content">{{ confidenceLevel.level }}</span>
    </b-popover>
    <span :id="id">
        <b-icon-star-fill  v-for="(star, idx) in confidenceLevel.stars" :key="idx" class="star" font-scale=".9"></b-icon-star-fill>
    </span>
    <!-- <svg :id="id" width="20" height="20">
      <circle :fill="confidenceLevel.color" cx="10" cy="10" r="8"></circle>
    </svg> -->
  </div>
</template>
<script>
import { FormatMixin } from "@/components/mixins/FormatMixin";
import * as _ from "lodash";
import { mapGetters } from "vuex";
export default {
  props: ["id", "attr", "confidence_values", "title"],
  mixins: [FormatMixin],
  data(){
    return {
      levels: {
        0: {level: 'Not available', stars: 0},
        1: {level:'High confidence', stars: 3},
        2: {level:'Medium confidence', stars: 2},
        3: {level:'Low confidence', stars: 1}
      }
    }
  },
  computed: {
    wrapStars(){
      return this.attribute.split(' ').length > 3;
    },
    attribute(){
      return this.formatAttribute(this.attr);
    },
    confidenceValue(){
      let conf_val = ''
      if (this.confidence_values.length){
        let confidence = _.filter(this.confidence_values, conf => {
          return conf.class_str === this.attr;
        });
        if(confidence.length){
          conf_val = parseFloat(confidence[0].confidence).toFixed(4);
        }
      }
      return conf_val;
    },
    confidenceLevel(){
      let level = this.levels['0'];
      if(this.confidence_values.length){
        let confidence = _.filter(this.confidence_values, conf => {
          return conf.class_str === this.attr;
        });
        if(confidence.length){
          let conf_level = confidence[0].bucket;
          if(Object.keys(this.levels).includes(String(conf_level))){
            level = this.levels[String(conf_level)];
          }
        }
      }
      return level;
    },
    ...mapGetters({
      aoi: "maps/getSelectedAoi"
    }),
  }
}
</script>
<style scoped>
.p-content {
  font-family: "Roboto Medium", sans-serif;
}
.star {
  color: lightgrey;
}
</style>
