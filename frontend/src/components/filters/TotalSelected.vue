<template>
  <div>
    <div v-if="show" class="total-total mb-2">Total buildings: {{ totalSelected }}</div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  props: ["map"],
  data(){
    return {
      show: false
    }
  },
  computed: {
    ...mapGetters({
      filters: "filters/getFilters",
      surveyFilters: "filters/getSelectedSurveyFilters"
    }),
    totalSelected(){
      let params = this.filters.length === 1 ? {sourceLayer: ['default']} : { sourceLayer: ['default'], filter: this.filters}
      let count = null;
      try {
        count = this.map.querySourceFeatures("buildings", params).length;
      }
      catch(Error){
        console.warn(Error, this.filters);
      }
      return count;
    }
  },
  created(){
    let vm = this;
    this.$root.$on('run-filters', () => {
      vm.show = true;
    })
    this.$root.$on('reset-map', () => {
      vm.show = false;
    })
  }
}
</script>

<style scoped>
.total-total {
  font-family: "Roboto Medium", sans-serif;
  padding: .5em;
  border: 1px solid black;
}

</style>
