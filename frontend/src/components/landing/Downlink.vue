<template>
  <div id="downlink" class="mx-auto d-flex align-items-center justify-content-center">
    <a href="#" v-scroll-to="'#what'">
      <b-icon class="icon" icon="chevron-down"></b-icon>
    </a>
  </div>
</template>
<script>
export default {

}
</script>
<style scoped>
@media (max-width: 639px), (orientation: portrait) {
  #downlink a {
    display: none;
  }
}
@media (min-width: 640px) {
  .icon {
    color: white;
    width: 40px;
    height: 40px;
  }
}
@media (min-width: 1200px) {
  .icon {
    color: white;
    width: 80px;
    height: 80px;
  }
}
#downlink {
  position: absolute;
  text-decoration: none;
  cursor: pointer;
  z-index: 900;
  max-height: 100vh;
  bottom: calc(100vh - 95vh);
  left: 0;
  right: 0;
}

</style>
