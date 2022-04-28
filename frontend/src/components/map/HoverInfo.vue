<template>
<div class="d-flex align-items-center justify-content-center">
  <b-alert v-if="show && map" id="alert" variant="light" class="text-center" show>
    <span class="title">{{ template.title }}: </span>
    <span class="message" v-html="template.msg"></span>
  </b-alert>
</div>

</template>
<script>
import numeral from "numeral";
import { FormatMixin } from "@/components/mixins/FormatMixin";
export default {
  props: ["map"],
  mixins: [FormatMixin,],
  data(){
    return {
      show: false,
      feature: null,
      template: null,
    }
  },
  methods: {
    getTemplate(feature){
      if(feature.layer.id === 'aoi'){
          let name = feature.properties.name;
          this.template = {
            title: 'Area of Interest',
            msg: `${name}`
          }
          return;
      }
      if(feature.layer.id === 'sectors'){
          let name = feature.properties.name;
          this.template = {
            title: 'Sector',
            msg: `${name}`
          }
          return;
      }
      if(feature.layer.id === 'greenspaces'){
          var area = this.formatGreenspace(feature.properties.area_m);
          this.template = {
            title: 'Greenspace',
            msg: `Area ${area}`
          }
          return;
      }
      if(feature.layer.id === 'buildings'){
          var addr = feature.properties.address;
          var address = addr !== '' ? addr : 'Unknown';
          if(address){
            this.template = {
              title: 'Building Address',
              msg: `${address}`
            }
          }
          return;
      }
    }
  },
  created(){
    let _vm = this;
    _vm.$root.$on('hover-info-show', feature => {
      this.show = true;
      this.getTemplate(feature);
    });
    _vm.$root.$on('hover-info-close', () => {
      this.show = false;
      this.html = null;
    })
  }
}
</script>
<style scoped>
#alert {
  position: absolute;
  top: 60px;
  width: auto;
  height: auto;
  font-size: .8em;
  padding: .3em .4em .3em .4em;
  z-index: 500;
  /* display: block; */
  outline: none;
  box-sizing: border-box;
  /* box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1); */
  -webkit-box-shadow: 3px 3px 3px 0px rgba(0, 0, 0, 0.3);
  -moz-box-shadow: 3px 3px 3px 0px rgba(0, 0, 0, 0.3);
  box-shadow: 3px 3px 3px 0px rgba(0, 0, 0, 0.3);
}
#alert > .title {
  font-weight: 600;
}
</style>
