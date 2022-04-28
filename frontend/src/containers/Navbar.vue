<template>
  <b-navbar id="navbar" toggleable="lg">
    <b-navbar-brand class="text-transform-uppercase">
      <b-container class="logos">
        <b-link to="/" class="p-0">
          <b-img id="img-gprh" src="/img/gprh_logo.png" fluid></b-img>
        </b-link>
        <b-link to="/" class="p-0">
          <b-img id="img-wb" src="/img/wb_logo.png" fluid></b-img>
        </b-link>
      </b-container>
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="mr-auto">
        <b-nav-text class="pl-2 pr-2">
          <span class="text-info font-weight-bolder">HOUSING PASSPORT</span>
          <span class="text-muted font-weight-bolder pl-2 pr-2"> | </span>
          <span class="text-uppercase font-weight-bolder">{{ country }}</span>
          <span class="text-muted font-weight-bolder pl-2 pr-2"> | </span>
          <template v-if="aoi">
            <template v-if="aoi.name === aoi.city" class="pl-2"><span></span></template>
            <template v-else >
              <span class="text-uppercase font-weight-bolder text-muted">{{ aoi.city }}</span>
              <span class="text-muted font-weight-bolder pl-2 pr-1"> | </span>
            </template>
          </template>
        </b-nav-text>
        <b-nav-form>
          <aoi-select  @aoi-selected="aoiSelected()"></aoi-select>
          <!-- <b-input-group id="aoi-select" size="sm">
            <b-form-select id="aoi-select" v-model="selectedAoi" :options="options" @change="aoiSelected()">
              <template v-slot:first>
                <option :value="null" disabled><span>Please select an Area of Interest <b-icon-caret-down-fill></b-icon-caret-down-fill></span></option>
              </template>
            </b-form-select>
          </b-input-group> -->
        </b-nav-form>
      </b-navbar-nav>
        <!-- <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">ES</b-dropdown-item>
          <b-dropdown-item href="#">RU</b-dropdown-item>
          <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown> -->
        <b-navbar-nav>
        <template v-if="loggedIn && !logoutPage">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template slot="button-content">
              <!-- <b-avatar size="sm" variant="info" v-if="loggedIn"></b-avatar> -->
              <span class="text-info"> Hello {{ profile.full_name.split(" ")[0] }} </span>
              <!-- <b-badge v-if="isAdmin" variant="danger">Admin</b-badge> -->
            </template>
            <b-dropdown-item @click="showDownloads()">Download datasets</b-dropdown-item>
            <b-dropdown-item v-if="isAdmin && aoi" :href="droneUrl" target="_blank">{{ aoi.name }} Drone Imagery</b-dropdown-item>
            <b-dropdown-item v-if="isAdmin" href="/admin/">Administer Users</b-dropdown-item>
            <b-dropdown-item href="/user-docs/" target="_blank">User Guide</b-dropdown-item>
            <b-dropdown-item v-if="isAdmin" href="/dev-docs/" target="_blank">Developer documentation</b-dropdown-item>
            <b-dropdown-item to="/logout">Logout</b-dropdown-item>
          </b-nav-item-dropdown>
        </template>
      </b-navbar-nav>
      <!-- <b-badge variant="success" class="nl-2 mr-2">Beta v0.1</b-badge> -->
    </b-collapse>
  </b-navbar>
</template>
<script>
import { mapState } from 'vuex'
import AOISelect from "@/components/nav/AOISelect"
export default {
  data(){
    return {
      aois: []
    }
  },
  computed: {
    selectedAoi: {
      get () {
        return this.$store.state.maps.selectedAOI;
      },
      set (value) {
        this.$store.commit('maps/setSelectedAoi', value);
      }
    },
    country() {
      return process.env.VUE_APP_PORTAL_COUNTRY;
    },
    options(){
      let options = [];
      let grouped = _.groupBy(this.aois, 'city');
      for(let city of Object.keys(grouped)){
        let group = {};
        group.label = city;
        let entries = [];
        for(let aoi of grouped[city]){
          let entry = {};
          entry.value = aoi;
          entry.text = aoi.name;
          entries.push(entry);
        }
        group.options = entries;
        options.push(group)
      }
      return options;
    },
    aoi() {
      return this.$store.getters["maps/getSelectedAoi"];
    },
    profile(){
      return this.$store.getters['getProfile']
    },
    loggedIn(){
      return this.$store.getters['isLoggedIn']
    },
    isAdmin() {
      return this.profile.is_admin;
    },
    loginPage(){
      return this.$route.name === 'Login'
    },
    logoutPage(){
      return this.$route.name === 'Logout'
    },
    droneUrl(){
      return "/drone-viewer/" + this.aoi.slug + ".html"
    }
  },
  methods: {
    async loadAois(){
      await this.$store.dispatch("maps/loadAOIS");
      this.aois = this.$store.getters["maps/getAois"];
    },
    aoiSelected(){
      this.$emit('aoi-selected');
    },
    showDownloads(){
      this.$emit('show-downloads');
    }
  },
  created(){
    this.loadAois();
  },
  components: {
    aoiSelect: AOISelect
  }
};
</script>
<style scoped>
nav {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  /* opacity: 0.85; */
  padding: 0px;
  border-bottom: 1px solid black;
  background-color: white;
  /* -webkit-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75); */
}
.navbar-brand {
  background-color: black;
  padding: 0px !important;
  margin-right: .5rem !important;
}
.logos {
  position: relative;
  top: 0;
  left: 0;
  width: 365px;
  height: 41px;
  padding: 0px 10px 0px 5px;
  /* padding: 0 15px 0 10px; */
}
#img-gprh {
  height: 20px;
  padding-right: 10px;
}
#img-wb {
  height:26px;
}
@media (max-width: 400px){
  .logos {
    width: 220px;
  }
}
.text-info {
  color: #CF5F5C!important;
  font-size: 1em;
  font-family: 'Roboto Regular', sans-serif;
  font-weight:bolder;
}
@media (min-width: 990px) and (max-width: 1365px){
  .text-info {
    display: none;
  }
}
#aoi-select {
  border: none;
  background: none !important;
}
#aoi-select > .custom-select:focus {
  border: none !important;
  box-shadow: none !important;
  -webkit-box-shadow: none !important;
}
#aoi-select > option {
  font-size: 1em !important;
  font-family: 'Roboto Regular', sans-serif !important;
  font-weight:bolder !important;
}
</style>
