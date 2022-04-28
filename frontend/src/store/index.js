import Vue from "vue";
import Vuex from "vuex";

// import users from "@/store/services/users";
import auth from "@/store/modules/auth";
import maps from "@/store/modules/maps/maps";
import analysis from "@/store/modules/analysis/analysis";
import filters from "@/store/modules/filters";
import downloads from "@/store/modules/downloads/download";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    // users,
    auth,
    maps,
    downloads,
    analysis,
    filters
  },
  plugins: [
    createPersistedState({
      paths: ["auth"]
    })
  ]
});

export default store;
