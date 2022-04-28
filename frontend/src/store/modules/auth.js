import axios from "axios";

let authAxios = axios.create({
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true
});

const state = {
  loggedIn: false,
  profile: {},
  validation: { email: true },
  authError: false
};

const getters = {
  getProfile(state) {
    return state.profile;
  },
  isLoggedIn(state) {
    return state.loggedIn;
  }
};

const mutations = {
  login(state) {
    state.loggedIn = true;
  },
  logout(state) {
    state.loggedIn = false;
  },
  setProfile(state, payload) {
    state.profile = payload;
  },
  setValidationEmail(state, bool) {
    state.validation.email = bool;
  },
  setAuthError(state, bool) {
    state.authError = bool;
  }
};

const actions = {
  checkLogin({ dispatch, commit }) {
    return authAxios
      .get("/api/check-user-login/")
      .then(async response => {
        await dispatch("getProfile");
      })
      .catch(e => {
        commit("logout");
        commit("setProfile", {});
      });
  },
  postLogin({ dispatch, commit }, payload) {
    return authAxios.post("/api/users/login/", payload).then(response => {
      dispatch("getProfile");
    });
  },
  postLogout({ commit, dispatch }, vm) {
    return authAxios
      .post("/api/users/logout/")
      .then(response => {
        commit("logout");
        commit("setProfile", {});
      })
      .catch(e => {
        commit("setAuthError", true);
        console.log(e);
      });
  },
  postRegister(context, payload) {
    return authAxios
      .post("/api/users/register/", payload)
      .then(response => {
        if (response.data.status === 210) {
          context.commit("setValidationEmail", false);
        } else {
          context.commit("setValidationEmail", true);
          context.commit("login");
          context.commit("setProfile", response.data);
        }
      })
      .catch(e => {
        console.log(e);
      });
  },
  async getProfile(context) {
    return await authAxios
      .get("/api/users/profile/")
      .then(response => {
        context.commit("login");
        context.commit("setProfile", response.data);
      })
      .catch(e => {
        context.commit("logout");
        console.log(e);
      });
  }
};

export default {
  state,
  getters,
  mutations,
  actions
};
