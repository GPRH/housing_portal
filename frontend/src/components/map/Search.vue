<template>
<div>
  <div id="address-search" v-if="aoi">
    <b-input-group>
      <template v-slot:prepend>
        <b-input-group-text id="searchIcon" @click="showSearch()" title="Open Search">
          <b-icon-search font-scale="1.1" variant="dark"></b-icon-search>
        </b-input-group-text>
      </template>
      <b-form-input
        id="search"
        ref="search"
        v-model="query"
        placeholder="Search"
        autocomplete="off"
        type="search"
        @input="search()"
        @blur="close()"
        @keydown.esc="close()"
        :disabled="!enabled"
      ></b-form-input>
    </b-input-group>
    <b-list-group v-show="showResults" class="autocomplete-results">
      <b-list-group-item v-if="results.mapbox.length" disabled class="result-header">
        <b-icon-geo-alt-fill></b-icon-geo-alt-fill> Search Results
      </b-list-group-item>
      <b-list-group-item v-for="(result, idx) in results.mapbox" :key="idx"
          @click="setResult(result, 'mapbox')">
        {{ result.place_name }}
      </b-list-group-item>
      <b-list-group-item v-if="results.local.length" disabled class="result-header">
        <b-icon-building></b-icon-building> Building Addresses
      </b-list-group-item>
      <b-list-group-item v-for="(result, idx) in results.local" :key="idx"
          @click="setResult(result, 'local')">
        {{ result.properties.address }}, {{ result.properties.sector_name }}, {{ result.properties.aoi_name }}
      </b-list-group-item>
    </b-list-group>
  </div>
</div>
</template>
<script>
import { mapGetters } from "vuex";
import Scroll from "@/components/analysis/Scroll"
import {filterBuildings} from "@/components/filters"
import { updateMapillaryMarker } from "@/components/mapillary";
export default {
  props: ["map"],
  data(){
    return {
      query: "",
      searchOpen: false,
      results: {mapbox: [], local: []}
    }
  },
  components: {
    appScroll: Scroll
  },
  computed: {
    ...mapGetters({
      displayLayers: "maps/getDisplayLayers",
    }),
    aoi(){
      return this.$store.getters['maps/getSelectedAoi'];
    },
    showResults() {
      return this.results.mapbox.length || this.results.local.length;
    },
    enabled(){
      let buildings = _.filter(this.displayLayers, layer => {
        return layer.id === 'buildings' && layer.checked === true;
      })
      return buildings.length > 0;
    }
  },
  methods: {
    async search(){
      if(this.query.length === 0){
        this.results = {mapbox: [], local: []};
        this.map.setFilter('buildings', null);
        this.$root.$emit('searching', false);
        return;
      }
      if(this.query.length > 3){
        let center = this.map.getCenter();
        let results = await this.$store.dispatch("maps/search", { query: this.query, proximity: center });
        this.results = results;
        this.$root.$emit('searching', true);
      }
    },
    showSearch(){
      if (this.query && this.searchOpen){
        return;
      }
      this.query = "";
      this.searchOpen = true;
      this.$nextTick(() => {
        this.$refs.search.focus();
      });
    },
    close(){
      if(!this.query){
        this.searchOpen = false;
      }
    },
    setResult(result, type){
      if(type === 'mapbox'){
        this.query = result.place_name;
        this.results = {mapbox: [], local: []};
        var center = result.center;
        // updateMapillaryMarker(this, center);
        // filterBuildings(this, 'building_id', result.properties.building_id);
        this.map.easeTo({center: [center[0], center[1]], zoom: 20});
      }
      else{
        this.query = result.properties.address;
        this.results = {mapbox: [], local: []};
        var center = result.properties.center;
        // updateMapillaryMarker(this, center);
        filterBuildings(this, 'uid', result.properties.uid);
        this.map.easeTo({center: [center[0], center[1]], zoom: 20});
        this.$root.$emit("address-selected", center);
        this.$store.dispatch("maps/selectFeature", {
          vm: this,
          feature: result,
          layer: "buildings"
        });
      }
      this.$root.$emit('searching', true);
    }
  },
  created(){
    let vm = this;
    this.$root.$on('reset-map', () => {
      vm.query = '';
      vm.results = {mapbox: [], local: []};
    });
  }
}
</script>
<style scoped>
#address-search {
  /* position: absolute; */
  /* top: 60px; */
  /* left: 10px; */
  /* max-width: 350px; */
  width: auto;
  pointer-events: all;
  border-bottom: 1px solid lightgrey;
}
#search {
  width: auto;
  border: none !important;
  background-color: white;
}
#searchIcon {
  /* border-top-left-radius: 0;
  border-bottom-left-radius: 0; */
  background-color: white;
  color: darkgrey;
  height: calc(1.5em + 0.75rem + 2px);
}
#searchIcon :hover {
  cursor: pointer;
}
#address-search .form-control:focus {
  -webkit-box-shadow: none;
  box-shadow: none;
}
#address-search .input-group-text {
  border: none !important;
  padding: 0px;
}
.autocomplete-results {
  position: relative;
  top: 0;
  left: 0;
  padding: 0;
  margin: 0;
  border: 1px solid #eeeeee;
  border-top: none;
  border-bottom: none;
  max-height: 150px;
  background-color: #FFF;
  overflow-y: scroll;
  width: auto;
  border-radius: 0px;
}
.result-header {
  padding: .2em;
}
.autocomplete-result {
  text-align: left;
  padding: 4px 2px;
  cursor: pointer;
}
.list-group-item:hover {
  background-color: whitesmoke;
  color: #000;
  cursor: pointer;
}
.list-group-item {
  padding: .2rem;
  font-size: .9em;
}
</style>
