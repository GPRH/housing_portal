<template>
  <div id="map-indicator" class="d-flex flex-column justify-content-center align-items-center">
    <b-overlay
      :show="loading"
      rounded
      opacity="0.6"
      class="d-inline-block"
    >
    <template v-slot:overlay>
      <b-spinner id="spinner" variant="info" :class="maximized ? 'maximized' : 'minimized'"  type="grow"></b-spinner>
    </template>
    </b-overlay>
  </div>
</template>
<script>
export default {
  props: ['maximized'],
  data(){
    return {
      loading: false
    }
  },
  created(){
    let _vm = this;
    this.$root.$on('mapillary-data-loading', loading => {
      _vm.loading = loading;
    });
    this.$root.$on('analysis-data-loading', loading => {
      _vm.loading = loading;
    });
  }
}
</script>
<style scoped>
#map-indicator {
  position: absolute;
  background: transparent;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
#spinner.maximized {
  width: 10rem;
  height: 10rem;
}
#spinner.minimized {
  width: 6rem;
  height: 6rem;
}
</style>
