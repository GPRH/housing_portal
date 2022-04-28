import Vue from "vue";
import store from "@/store/index";
import router from "@/routes";
import VeeValidate from "vee-validate";
import VueScrollTo from "vue-scrollto";
import PerfectScrollbar from "vue2-perfect-scrollbar";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "vue2-perfect-scrollbar/dist/vue2-perfect-scrollbar.css";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
Vue.component("v-select", vSelect);
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
Vue.component("VueSlider", VueSlider);

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(PerfectScrollbar, {
  name: "scroll"
});
Vue.use(VueScrollTo, {
  container: "body",
  duration: 500,
  easing: "ease",
  offset: 0,
  force: true,
  x: false,
  y: true
});

import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

import App from "@/App.vue";

Vue.config.productionTip = false;

Vue.use(VeeValidate, {
  inject: true,
  fieldsBagName: "veeFields",
  classes: true,
  classNames: {
    valid: "is-valid",
    invalid: "is-invalid"
  }
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
