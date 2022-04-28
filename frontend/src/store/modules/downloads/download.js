import axios from "axios";

let authAxios = axios.create({
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true
});

const state = {};

const getters = {};

const mutations = {};

const actions = {
  postPreparedDownload(context, payload) {
    return authAxios.post("/api/geodata/download/", payload);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
