<template>
  <b-toast id="mapillary-warning"
    :style="style"
    :visible="show"
    variant="warning"
    auto-hide-delay=5000
    @hide="show = false"
    toaster="b-toaster-bottom-center"
    no-close-button
    title="Street View Warning" solid>
    <template v-slot:default>
      <span v-html="message" class="text-dark"></span>
    </template>
  </b-toast>
</template>

<script>
export default {
  props:["map", "maximized"],
  data(){
    return {
      show: false,
      coords: null,
      message: `<p>No panoramic images are available at the selected location.</p>`,
    }
  },
  computed: {
    style(){
      return {
        top: `${this.location.y}px`,
        left: `${this.location.x + 50}px`
      }
    },
    location() {
      if(this.map && this.coords){
        return this.map.project(this.coords);
      }
      return [0,0];
    }
  },
  created(){
    this.$root.$on('mapillary-warning', payload => {
      let { show, coords } = payload;
      this.show = show;
      this.coords = coords;
    })
  }
}
</script>

<style scoped>
#mapillary-warning {
  z-index: 2000;
  max-width: 200px;
  opacity: .9;
  top: 100px !important;
}

</style>
