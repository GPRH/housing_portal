import Vue from "vue";
import VueRouter from "vue-router";

import Landing from "@/views/landing/Landing.vue";
import MapViewer from "@/views/maps/MapViewer.vue";
import Login from "@/views/users/Login.vue";
import Logout from "@/views/users/Logout.vue";
import NotFound from "@/views/404.vue";

import store from "@/store/index";

const routes = [
  {
    path: "*",
    name: "NotFound",
    component: NotFound
  },
  {
    path: "/",
    name: "Landing",
    component: Landing,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/portal",
    name: "MapViewer",
    component: MapViewer,
    meta: {
      requiresAuth: true
    }
  },
  // {
  //   path: "/portal/:aoiSlug/:geohash",
  //   name: "MapViewerPermalink",
  //   component: MapViewer,
  //   props: true,
  //   meta: {
  //     requiresAuth: true
  //   }
  // },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/logout",
    name: "Logout",
    component: Logout
  }
];

Vue.use(VueRouter);
const router = new VueRouter({
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
  mode: "history",
  routes
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    await store.dispatch("checkLogin");
    if (store.getters.isLoggedIn || to.name === "Landing") {
      next();
    } else {
      next("/login");
    }
  } else {
    next();
  }
});

export default router;
