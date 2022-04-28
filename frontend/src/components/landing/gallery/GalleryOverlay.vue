<template>
  <b-overlay :show="show" :map="map" variant="dark" opacity=".85" blur="2px" no-wrap no-center>
    <template #overlay>
      <b-container fluid>
        <b-row>
          <b-col cols="10">
            <span class="float-left text-light map-text">{{ text }}</span>
          </b-col>
          <b-col cols="2">
            <b-icon icon="x-circle" class="float-right close text-light" @click="hide()"></b-icon>
          </b-col>
        </b-row>
        <b-row no-gutters>
          <b-col>
            <b-img :src="img" fluid-grow></b-img>
          </b-col>
        </b-row>
      </b-container>
    </template>
  </b-overlay>
</template>

<script>
export default {
  props: ["show", "map"],
  data(){
    return {
      config: {
        bogota: {
          img: '/img/gallery/overlays/bogota-1500x776.png',
          text: 'The COVID-19 Vulnerability Index: Locating the 40% most vulnerable in Bogota, Colombia.'
        },
        lima: {
          img: '/img/gallery/overlays/lima-1500x776.png',
          text: 'Locating homes that are overcrowded in Lima, Peru.'
        },
        mexico: {
          img: '/img/gallery/overlays/salinacruz-1500x776.png',
          text: 'Locating homes built with unreinforced masonry in Salina Cruz, Mexico.'
        },
        chacarita: {
          img: '/img/gallery/overlays/chacarita-1500x776.png',
          text: 'Locating homes that face high flood risk in Chacarita, Asuncion, Paraguay.'
        },
        stlucia: {
          img: '/img/gallery/overlays/stlucia-1500x776.png',
          text: 'Locating homes that need roof retrofitting to withstand hurricanes in Castries, St. Lucia.'
        },
        guatemala: {
          img: '/img/gallery/overlays/guatemala-1500x776.png',
          text: 'Locating homes that have dirt floors in Guatemala City.'
        },
        stmaarten: {
          img: '/img/gallery/overlays/stmaarten-1500x776.png',
          text: 'Locating backyard homes in Philipsburg, Sint Maarten.'
        },
        padang: {
          img: '/img/gallery/overlays/padang-1500x776.png',
          text: 'Locating homes constructed with reinforced masonry in Padang, Indonesia.'
        },
        limatax: {
          img: '/img/gallery/overlays/lima-taxes-1500x776.png',
          text: 'Locating units that have not paid property taxes in Lima, Peru.'
        }
      }
    }
  },
  computed: {
    img(){
      return this.config[this.map].img;
    },
    text(){
      return this.config[this.map].text;
    }
  },
  methods: {
    hide(){
      this.$emit('hide-overlay');
    }
  }
}
</script>

<style scoped>
.map-text {
  padding: .5em 0 .5em 0;
  font-size: 3vh;
}
.close {
  margin: .5em 0 .5em 0;
  cursor: pointer;
  font-size: 4vh;
}
</style>
