<template>
  <b-container id="navwrapper" fluid>
    <b-navbar id="navbar" toggleable="md">
      <b-navbar-brand
        href="#"
        class="text-transform-uppercase"
      >
        <b-container class="d-flex justify-content-start">
          <b-row class="p-0">
            <b-col class="p-0"><b-img src="img/landing/WB_Logo.png" fluid/></b-col>
            <b-col class="p-0"><b-img src="img/landing/Logo_GPRH_white.png" fluid/></b-col>
          </b-row>
        </b-container>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <!-- <b-nav-item-dropdown text="Lang" right>
            <b-dropdown-item href="#">EN</b-dropdown-item>
            <b-dropdown-item href="#">ES</b-dropdown-item>
            <b-dropdown-item href="#">RU</b-dropdown-item>
            <b-dropdown-item href="#">FA</b-dropdown-item>
          </b-nav-item-dropdown> -->
          <!-- <b-nav-item-dropdown right v-if="loggedIn && !logoutPage" class="text-light">
            <template slot="button-content">
              <b-avatar size="sm" variant="info" v-if="loggedIn"></b-avatar>
              <em> {{ profile.full_name }} </em><b-badge v-if="isAdmin" variant="danger">Admin</b-badge>
            </template>
            <b-dropdown-item v-if="isAdmin" href="/admin/">Administer Users</b-dropdown-item>
            <b-dropdown-item v-if="isAdmin" href="/docs/" target="_blank">Platform documentation</b-dropdown-item>
            <b-dropdown-item to="/logout">Logout</b-dropdown-item>
          </b-nav-item-dropdown> -->
          <!-- <b-nav-item v-if="loggedIn">
            <b-button variant="success" size="sm" to="/portal">
              Go To Portal
            </b-button>
          </b-nav-item> -->

          <b-nav-item v-if="!loggedIn" >
            <b-button class="login" size="md" to="/login">
              Log in
            </b-button>
          </b-nav-item>
          <b-nav-item v-else>
            <b-button class="go-portal" variant="success" size="md" to="/portal">
            Go to portal
          </b-button>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </b-container>
</template>
<script>
import { mapState } from 'vuex'
export default {
  data(){
    return {
      aois: []
    }
  },
  computed: {
    country() {
      return process.env.VUE_APP_PORTAL_COUNTRY;
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
  },
};
</script>
<style scoped>
#navwrapper {
  z-index: 100;
  position: absolute;
  top: 25px;
  left: 0;
  background-color: transparent;
}
nav {
  height: 40px;
}
.login {
  z-index: 500;
  border-radius: 0px;
  line-height: .8rem;
  background-color: #F60021;
  padding: .3 .6em .3em .6em;
  border: 1px solid #F60021;
  width: 100px;
  font-size: .9rem;
}
.login:hover {
  background-color: #c82333;
  border: 1px solid #c82333;
}
.go-portal {
  z-index: 500;
  border-radius: 0px;
  line-height: .8rem;
  padding: .3 .6em .3em .6em;
  width: 125px;
  font-size: .9rem;
}
.logos {
  position: absolute;
  top: 0px;
  left: 0px;
  max-width: 40%;
}
</style>
