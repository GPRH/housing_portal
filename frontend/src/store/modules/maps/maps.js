import * as actions from "./actions";
import * as _ from "lodash";
import { baseLayers } from "./layers";
import { legends } from "./legends";
import { config } from "./config";

const PORTAL_COUNTRY = process.env.VUE_APP_PORTAL_COUNTRY.toLowerCase();

const state = {
  config: config,
  aois: null,
  selectedAOI: null,
  selectedBaseLayer: baseLayers[0],
  layers: [],
  legends: legends,
  displayLayers: [],
  baseLayers: baseLayers,
  bounds: null,
  defaultBounds: process.env.VUE_APP_PORTAL_EXTENTS.split(" "),
  defaultCenter: process.env.VUE_APP_PORTAL_CENTER.split(" "),
  selectedFeature: null
};

const mutations = {
  setAois(state, aois) {
    state.aois = aois;
  },
  setSelectedAoi(state, aoi) {
    state.selectedAOI = aoi;
  },
  setBaseLayer(state, baseLayer) {
    state.selectedBaseLayer = baseLayer;
  },
  addLayer(state, layer) {
    state.layers.unshift(layer);
  },
  removeLayer(state, layer) {
    let filtered = _.filter(state.layers, lyr => {
      return lyr.id !== layer.id;
    });
    state.layers = filtered;
  },
  setLayers(state, layers) {
    state.layers = layers;
  },
  setDisplayLayers(state, layers) {
    state.displayLayers = layers;
  },
  setBounds(state, bounds) {
    state.bounds = bounds;
  },
  clearLayers(state) {
    state.layers = [];
    state.displayLayers = [];
  },
  selectFeature(state, selectedFeature) {
    if (selectedFeature) {
      let { feature, layer } = selectedFeature;
      if (layer === "aoi") {
        state.selectedAOI.feature = selectedFeature;
      }
    }
    state.selectedFeature = selectedFeature;
  }
};

const getters = {
  getConfig: state => {
    return state.config[PORTAL_COUNTRY];
  },
  getAoiConfig: state => {
    return state.config[PORTAL_COUNTRY][state.selectedAOI.slug];
  },
  getAois: state => {
    return state.aois;
  },
  getSelectedAoi: state => {
    return state.selectedAOI;
  },
  getSelectedBaseLayer: state => {
    return state.selectedBaseLayer;
  },
  getLayer: state => layer => {
    let lyr = state.layers.find(element => element.id === layer);
    return lyr;
  },
  getLayers: state => {
    return state.layers;
  },
  getLegends: state => {
    return state.legends;
  },
  getDisplayLayers: state => {
    return state.displayLayers;
    // return _.sortBy(state.displayLayers, layer => {
    //   return layer.name;
    // });
  },
  getBounds: state => {
    return state.bounds;
  },
  getDefaultBounds: state => {
    return state.defaultBounds;
  },
  getDefaultCenter: state => {
    return state.defaultCenter;
  },
  getSelectedFeature: state => {
    return state.selectedFeature;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};
