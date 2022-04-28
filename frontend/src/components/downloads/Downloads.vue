<template>
<div id="dlwrap" class="d-flex align-items-stretch justify-content-center">
  <b-alert
    ref="downloads"
    id="downloads"
    variant="dark"
    v-if="show && !prepDownload"
    dismissible
    show
    @dismissed="dismiss"
  >
    <h3 class="mt-2 mb-2">Download data for {{ country }}</h3>
    <div class="row">
      <div class="col-md-6 mt-3">
        <b-button
          class="p-4 mb-2"
          block
          size="lg"
          v-for="btn in buttons"
          :pressed.sync="btn.state"
          :active="btn.state"
          variant="outline-primary"
          :key="btn.caption"
          @click="selectAoi(btn.value)"
        >{{ btn.caption }}</b-button>
      </div>
      <div class="col-md-6" v-if="aoi">
        <b-card class="mt-3">
          <h5>Select a dataset...</h5>
          <b-form-group>
            <b-form-radio-group v-model="dataset" stacked name="datasets" size="sm">
              <!-- <b-form-radio value="all">All datasets</b-form-radio> -->
              <b-form-radio value="sectors">Sectors</b-form-radio>
              <!-- <b-form-radio value="blocks">Blocks</b-form-radio> -->
              <b-form-radio value="buildings">Buildings</b-form-radio>
              <b-form-radio value="greenspace">Greenspace</b-form-radio>
              <!-- <b-form-radio value="roads">Roads</b-form-radio> -->
            </b-form-radio-group>
          </b-form-group>
        </b-card>
        <b-card class="mt-3">
          <h5>Select a download format...</h5>
          <b-form-select v-model="format" :options="formats" size="sm" class="mb-3"></b-form-select>
        </b-card>
        <div class="row mt-3 mb-3">
          <div class="col-md-4">
            <b-button
              size="md"
              variant="success"
              block
              :disabled="aoi === null || dataset === null || format === null"
              @click="download()"
            >
              Next
            </b-button>
          </div>
          <div class="col-md-4">
            <b-button size="md" variant="warning" block @click="reset" :disabled="!aoi && !dataset">Reset</b-button>
          </div>
          <div class="col-md-4">
            <b-button size="md" variant="danger" block @click="dismiss">Cancel</b-button>
          </div>
        </div>
      </div>
      <div v-else class="p-3">
        <h4>Select an Area of Interest</h4>
      </div>
    </div>
  </b-alert>
  <b-alert
    ref="downloadResult"
    id="downloadResult"
    v-if="prepDownload"
    dismissible
    show
    class="alert-light"
    @dismissed="dismiss()"
  >
    <div v-if="!download_url" class="row mt-3 mb-3 align-items-center justify-content-center">
      <div class="col-md-12 text-center ">
        <h3>Preparing download</h3>
        <div class="mt-5">
            <b-spinner
              variant="success"
              style="width: 5rem; height: 5rem;"
            ></b-spinner>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="row mt-3 mb-3">
        <div class="col-md-12 text-center">
          <h3>Download your data</h3>
          <b-button size="lg" variant="primary" :href="download_url" class="mt-5" @click="dismiss()">
            <b-icon-arrow-down-circle-fill class=""></b-icon-arrow-down-circle-fill>  Download
          </b-button>
        </div>
        <div class="col-md-12 text-center" v-if="status === 204">
          <div class="alert alert-danger mx-auto w-50">
            <h4>No data available.</h4>
          </div>
        </div>
      </div>
    </div>
  </b-alert>
</div>
</template>
<script>
import * as _ from "lodash";

export default {
  props: ["show"],
  data() {
    return {
      aoi: null,
      dataset: null,
      format: null,
      download_url: null,
      prepDownload: false,
      status: null,
      formats: [
        { value: "geojson", text: "GeoJSON" },
        { value: "gpkg", text: "GeoPackage" },
        { value: "shp", text: "ESRI Shapefile" },
        { value: "csv", text: "CSV" }
      ],
      alldata: ["buildings", "blocks", "roads", "sectors", "greenspace"],
    };
  },
  computed: {
    aois(){
      return this.$store.getters["maps/getAois"];
    },
    buttons(){
      let btns = [];
      for(let aoi of this.aois){
        let option = {caption: aoi.name, state: false, value: aoi.slug }
        btns.push(option);
      }
      return btns;
    },
    btnStates() {
      return this.buttons.map(btn => btn.state);
    },
    country() {
      return process.env.VUE_APP_PORTAL_COUNTRY;
    },
  },
  methods: {
    dismiss() {
      this.$emit("dismissed");
      _.forEach(this.buttons, (val, key) => {
        val.state = false;
      });
      this.aoi = null;
      this.dataset = null;
      this.format = null;
      this.prepDownload = false;
      this.status = null;
      this.download_url = null;
    },
    reset(){
      this.aoi = null;
      this.dataset = null;
      this.format = null;
      _.forEach(this.buttons, (val, key) => {
        val.state = false;
      });
    },
    selectAoi(aoi) {
      this.aoi = aoi;
      _.forEach(this.buttons, (val, key) => {
        if (val.value === aoi) {
          val.state = true;
        } else {
          val.state = false;
        }
      });
    },
    // deprecated in favour of static downloads
    // https://github.com/bjohare/wb-housing-prototype/issues/121
    // leaving here in case we ever want to revert.
    //
    // async download() {
    //   this.prepDownload = true;
    //   this.$store
    //     .dispatch("downloads/postPreparedDownload", {
    //       aoi: this.aoi,
    //       dataset: this.dataset,
    //       format: this.format
    //     })
    //     .then(response => {
    //       if (response.status === 200) {
    //         this.download_url = response.data.download_url;
    //         this.status = response.status;
    //       }
    //     })
    //     .catch(error => {
    //       if (error.response) {
    //         let data = error.response.data;
    //         console.log(data);
    //       }
    //     });
    // },
    download() {
      this.prepDownload = true;
      let country = this.country.toLowerCase();
      let file = `${this.aoi}-${this.dataset}-${this.format}.zip`;
      this.download_url = `/api/geodata/exports/${country}/${this.aoi}/${file}`
    }
  }
};
</script>

<style>
#dlwrap {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
}
#downloads {
  position: absolute;
  top: 60px;
  z-index: 900;
  max-height: calc(100vh - 100px);
  width: 80%;
  opacity: 0.99;
  padding: 1rem;
  overflow: auto;
  color: black !important;
  background-color: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.2);
  pointer-events: all;
  font-family: "Roberto Medium", sans-serif;
}
#downloadResult {
  position: absolute;
  top: 60px;
  z-index: 900;
  width: 40%;
  opacity: 0.97;
  padding: 1rem;
  overflow: auto;
  color: black !important;
  background-color: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.2);
  pointer-events: all;
}
.card-body .custom-control-label {
  font-size: 1rem;
  font-weight: 600;
}
.custom-radio {
  padding: 1rem 0 0.2rem 2rem;
}
</style>
