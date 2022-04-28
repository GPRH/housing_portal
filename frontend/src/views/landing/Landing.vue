<template>
  <b-container id="landing-page" fluid class="p-0 d-flex align-items-center justify-content-center">
    <b-row no-gutters>
      <landing-nav></landing-nav>
      <jumbo></jumbo>
      <gallery></gallery>
      <info></info>
    </b-row>
  </b-container>
</template>
<script>
import LandingNav from "@/components/landing/LandingNav";
import Jumbo from "@/components/landing/Jumbo";
import Splash from "@/components/landing/Splash"
import Info from "@/components/landing/Info";
import MapGallery from "@/components/landing/gallery/MapGallery";
export default {
  data() {
    return {
    }
  },
  components: {
    landingNav: LandingNav,
    jumbo: Jumbo,
    splash: Splash,
    gallery: MapGallery,
    info: Info,
  }
}
</script>
<style scoped>

</style>
