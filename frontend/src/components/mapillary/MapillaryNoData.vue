<template>
  <div
    id="mapillary-nodata"
    class="d-flex flex-column justify-content-center align-items-center"
    :class="nodata ? 'active' : 'inactive'"
    v-show="nodata"
  >
    <b-overlay
      id="nodata-overlay"
      :show="nodata && !maximized"
      rounded
      opacity="0.8"
      blur="2px"
      variant="light"
      class="d-inline-block w-100 h-100"
    >
      <template v-slot:overlay>
        <div id="nodata-text" class="text-center">
          <div class="h2 text-info">
            <b-icon-exclamation-triangle-fill></b-icon-exclamation-triangle-fill></div>
            No street view available at this location.
        </div>
      </template>
    </b-overlay>
  </div>
</template>
<script>
export default {
  props: ["nodata", "maximized"],
}
</script>
<style scoped>
#mapillary-nodata {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1300 !important;
  pointer-events: none;
}
#mapillary-nodata.active {
  pointer-events: all;
}
#mapillary-nodata.inactive {
  pointer-events: none;
}
#nodata-text {
  font-family: 'Roboto Regular', sans-serif;
  font-size: 1.2em;
  font-weight: 500;
  height: 100%;
}

</style>
