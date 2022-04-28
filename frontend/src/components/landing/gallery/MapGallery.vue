<template>
  <b-container id="gallery" fluid>
      <a id="what" class="pt-2"></a>
      <h1 class="section-title mt-4">What we do</h1>
      <section class="content d-flex justfiy-content-center">
        <p class="content">
          We partner with governments and companies to support vulnerable households in making their
          homes safer and more resilient.
        </p>
      </section>
      <section>
        <div class="position-relative">
          <b-row>
            <b-col>
              <b-card @click="click('bogota')" @mouseover="bogotaHover = true" @mouseout="bogotaHover = false" class="map-card" img-src="img/gallery/thumbs/bogota-800x530.png" overlay img-alt="Covid 19 Vulerability, Lima, Peru.">
                <b-icon icon="plus-circle" v-show="bogotaHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">The COVID-19 Vulnerability Index: Locating the 40% more vulnerable in Bogota, Colombia.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card v-show="!limaHover" @mouseover="limaHover = true" class="map-card" img-src="img/gallery/thumbs/lima-800x530.jpg" overlay>
                <b-card-text class="transparent text-uppercase"><span class="yellow">375,000 overcrowded</span> homes <br/> in Lima, Peru.</b-card-text>
              </b-card>
              <b-card @click="click('lima')" v-show="limaHover" @mouseout="limaHover= false" class="map-card" img-src="img/gallery/thumbs/lima-800x530.png" overlay>
                <b-icon icon="plus-circle" v-show="limaHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes that are overcrowded in Lima, Peru.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card @click="click('mexico')" @mouseover="mexicoHover = true" @mouseout="mexicoHover = false" class="map-card" overlay img-src="img/gallery/thumbs/salinacruz-800x530.png">
                <b-icon icon="plus-circle" v-show="mexicoHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes built with unreinforced masonry in Salina Cruz, Mexico.</b-card-text>
              </b-card>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-card v-show="!chacaritaHover" @mouseover="chacaritaHover = true" class="map-card" overlay img-src="img/gallery/thumbs/paraguay-800x530.jpg">
                <b-card-text class="transparent text-uppercase"><span class="yellow text-uppercase">10,000 units</span> face <span class="yellow">high flood risk</span> in chacarita, asuncion, paraguay.</b-card-text>
              </b-card>
              <b-card @click="click('chacarita')" v-show="chacaritaHover" @mouseout="chacaritaHover = false" class="map-card" overlay img-src="img/gallery/thumbs/chacarita-800x530.png">
                <b-icon icon="plus-circle" v-show="chacaritaHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes that face high flood risk in Chacarita, Asuncion, Paraguay.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card @click="click('stlucia')" @mouseover="stluciaHover = true" @mouseout="stluciaHover = false" class="map-card" overlay img-src="img/gallery/thumbs/stlucia-800x530.png">
                <b-icon icon="plus-circle" v-show="stluciaHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes that need roof retrofiting to withstand hurricanes in Castries, St. Lucia.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card v-show="!guatemalaHover" @mouseover="guatemalaHover = true" class="map-card" overlay img-src="img/gallery/thumbs/guatemala-800x530.jpg">
                <b-card-text class="transparent text-uppercase"><span class="yellow">50,625</span> homes have <span class="yellow">dirt floors</span> in guatemala city.</b-card-text>
              </b-card>
              <b-card @click="click('guatemala')" v-show="guatemalaHover" @mouseout="guatemalaHover = false" class="map-card" overlay img-src="img/gallery/thumbs/guatemala-800x530.png">
                <b-icon icon="plus-circle" v-show="guatemalaHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes that have dirt floors in Guatemala City.</b-card-text>
              </b-card>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-card @click="click('stmaarten')" @mouseover="stmaartenHover = true" @mouseout="stmaartenHover = false" class="map-card" overlay img-src="img/gallery/thumbs/stmaarten-800x530.png">
                <b-icon icon="plus-circle" v-show="stmaartenHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating backyard homes in Philipsburg, Sint Maarten.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card v-show="!padangHover" @mouseover="padangHover = true" class="map-card" overlay img-src="img/gallery/thumbs/indonesia-800x530.jpg">
                <b-card-text class="transparent text-uppercase"><span class="yellow">92% of homes</span> have <span class="yellow">reinforced masonry</span> in Padang, indonesia.</b-card-text>
              </b-card>
              <b-card @click="click('padang')" v-show="padangHover" @mouseout="padangHover = false" class="map-card" overlay img-src="img/gallery/thumbs/padang-800x530.png">
                <b-icon icon="plus-circle" v-show="padangHover"  class="plus-circle"></b-icon>
                <b-card-text class="grey">Locating homes constructed with reinforced masonry in Padang, Indonesia.</b-card-text>
              </b-card>
            </b-col>
            <b-col>
              <b-card @click="click('limatax')" @mouseover="limaTaxHover = true" @mouseout="limaTaxHover = false" class="map-card" overlay img-src="img/gallery/thumbs/lima-taxes-800x530.png">
                <b-icon icon="plus-circle" v-show="limaTaxHover"  class="mr-auto plus-circle"></b-icon>
                <b-card-text class="grey">Locating units that have not paid property taxes in Lima, Peru.</b-card-text>
              </b-card>
            </b-col>
          </b-row>
          <gallery-overlay :show="showOverlay" :map="map" @hide-overlay="hideOverlay()"></gallery-overlay>
        </div>
      </section>
  </b-container>
</template>
<script>
import GalleryOverlay from "@/components/landing/gallery/GalleryOverlay";
export default {
  data(){
    return {
      bogotaHover: false,
      limaHover: false,
      mexicoHover: false,
      chacaritaHover: false,
      stluciaHover: false,
      stmaartenHover: false,
      guatemalaHover: false,
      padangHover: false,
      limaTaxHover: false,
      showOverlay: false,
      map: null,
    }
  },
  methods: {
    click(map){
      this.map = map
      this.showOverlay = true;
    },
    hideOverlay(){
      this.map = null;
      this.showOverlay = false;
    }
  },
  components: {
    galleryOverlay: GalleryOverlay
  }
}
</script>

<style scoped>
@media (min-width: 1200px) {
  #gallery {
    padding: 0 4em 0 4em;
  }
}
@media (max-width: 1024px){
  #gallery {
    padding: 0 2em 0 2em;
  }
  .card-text {
    font-size: 2vh !important;
  }
}
@media (max-width: 768px) {
  #gallery {
    padding: 0 2em 0 2em;
  }
  .card-text {
    display: none;
  }
}
.section-title {
  color: #e11921;
  margin-top: 40px;
  margin-bottom: 20px;
  font-family: 'Roboto Regular', sans-serif;
}
.col {
  margin-bottom: 1em;
}
.content {
  margin-left: 0px;
  font-size: 1.2em;
  font-family: 'Roboto Light', sans-serif;
  color: #555555;
}
.card {
  max-height: 325px;
}
.card-body {
  padding: 0;
  pointer-events: none;
}
.card-text {
  position: absolute;
  bottom: 0;
  padding: 0.5em;
  width: 100%;
  font-size: 2.5vh;
}
.map-card:hover {
  cursor: pointer;
}
.grey {
  background-color: #EFF1F2;
  color: #676768;
  font-family: 'Roboto Medium', sans-serif;
}
.transparent {
  background-color: transparent;
  color: white !important;
  text-align: center !important;
  font-size: 3vh;
}
.yellow {
  color: #FFDF00;
  font-weight: bold;
}
.inActive {
  display: none;
}
.active {
  display: block;
}
.plus-circle {
  width: 6vh;
  height: 6vh;
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -70%);
}
</style>
