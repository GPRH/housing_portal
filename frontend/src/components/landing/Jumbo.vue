<template>
<div>
  <a id="home"></a>
  <b-row no-gutters id="jubmo">
    <b-col col-md-12>
      <b-carousel
          id="landing-carousel"
          v-model="slide"
          controls
          indicators
          style="text-shadow: 1px 1px 2px #333;"
        >
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_1.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_2.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_3.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_4.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_5.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_6.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_7.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <b-carousel-slide>
          <template slot="img">
            <b-img class="landing-image" src="img/landing/Carousel_8.jpg" fluid width="1920px" height="1080px"></b-img>
          </template>
        </b-carousel-slide>
        <splash></splash>
        <downlink></downlink>
      </b-carousel>
    </b-col>
  </b-row>
</div>
</template>
<script>
import Downlink from "@/components/landing/Downlink";
import Splash from "@/components/landing/Splash";
export default {
  components: {
    downlink: Downlink,
    splash: Splash
  },
  data(){
    return {
      slide: 0
    }
  }
}
</script>
<style>
#jumbo {
  height:100vh;
}

@media (max-width: 639px) {
  ol.carousel-indicators {
    display: none;
  }
}
@media (min-width: 640px){
    ol.carousel-indicators {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 75px;
  }
  .carousel-indicators li {
    width: 10px !important;
    height: 10px !important;
    border-radius: 100% !important;
    background-color: #666666 !important;
    opacity: 1 !important;
  }
.carousel-indicators li.active {
    background-color: #b3b3b3 !important;
    opacity: 1 !important;
  }
}
@media (min-width: 1200px) {
    ol.carousel-indicators {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 105px;
  }
  .carousel-indicators li {
    width: 15px !important;
    height: 15px !important;
    border-radius: 100% !important;
    background-color: #666666 !important;
    opacity: 1 !important;
  }
.carousel-indicators li.active {
    background-color: #b3b3b3 !important;
    opacity: 1 !important;
  }
}

.carousel-control-prev-icon {
  position: absolute;
  left: 20px;
  width: 16px;
  height: 16px;
  color: white;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23fff' viewBox='0 0 16 16'%3e%3cpath d='M 11.354 1.646 a 0.5 0.5 0 0 1 0 0.708 L 5.707 8 l 5.647 5.646 a 0.5 0.5 0 0 1 -0.708 0.708 l -6 -6 a 0.5 0.5 0 0 1 0 -0.708 l 6 -6 a 0.5 0.5 0 0 1 0.708 0 Z'/%3e%3c/svg%3e") !important;
}
.carousel-control-next-icon {
  position: absolute;
  right: 20px;
  width: 16px;
  height: 16px;
  color: white;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23fff' viewBox='0 0 16 16'%3e%3cpath d='M 4.646 1.646 a 0.5 0.5 0 0 1 0.708 0 l 6 6 a 0.5 0.5 0 0 1 0 0.708 l -6 6 a 0.5 0.5 0 0 1 -0.708 -0.708 L 10.293 8 L 4.646 2.354 a 0.5 0.5 0 0 1 0 -0.708 Z'/%3e%3c/svg%3e") !important;
}
</style>
