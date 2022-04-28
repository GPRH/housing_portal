import { propertyFilters } from "./filters";
import { qualityFilters } from "./filters";
import { useFilters } from "./filters";
import { surveyFilters } from "./filters";
import * as actions from "./actions";

const state = {
  area: null,
  building: null,
  height: null,
  tax: null,
  taxOwed: null,
  k3: null,
  selectedPropertyFilters: [],
  selectedQualityFilters: [],
  selectedUseFilters: [],
  selectedSurveyFilters: [],
  propertyFilters: propertyFilters,
  qualityFilters: qualityFilters,
  useFilters: useFilters,
  surveyFilters: surveyFilters
};

const mutations = {
  setAreaFilter(state, area) {
    state.area = area;
  },
  setBuildingFilter(state, building) {
    state.building = building;
  },
  setHeightFilter(state, height) {
    state.height = height;
  },
  setTaxFilter(state, tax) {
    state.tax = tax;
  },
  setTaxOwedFilter(state, taxOwed) {
    state.taxOwed = taxOwed;
  },
  setK3Filter(state, k3) {
    state.k3 = k3;
  },
  setSelectedPropertyFilters(state, filters) {
    state.selectedPropertyFilters = filters === null ? [] : filters;
  },
  setSelectedQualityFilters(state, filters) {
    state.selectedQualityFilters = filters === null ? [] : filters;
  },
  setSelectedUseFilters(state, filters) {
    state.selectedUseFilters = filters === null ? [] : filters;
  },
  setSelectedSurveyFilters(state, filters) {
    state.selectedSurveyFilters = filters === null ? [] : filters;
  },
  setFilters(state, filters) {
    state.filters = filters;
  }
};

const getters = {
  getPropertyFilters: state => {
    return state.propertyFilters;
  },
  getQualityFilters: state => {
    return state.qualityFilters;
  },
  getUseFilters: state => {
    return state.useFilters;
  },
  getSurveyFilters: state => {
    return state.surveyFilters;
  },
  getFilters: state => {
    let filters = ["all"];
    let all_filters = [
      state.area,
      state.building,
      state.height,
      state.tax,
      state.taxOwed,
      state.k3
    ];
    for (let filter of all_filters) {
      if (filter === null) continue;
      filters.push(filter);
    }
    if (state.selectedPropertyFilters.length) {
      for (let filter of state.selectedPropertyFilters) {
        if (filter === null) continue;
        filters.push(filter.expression);
      }
    }
    if (state.selectedQualityFilters.length) {
      let quality_filters = ["any"];
      for (let filter of state.selectedQualityFilters) {
        if (filter === null) continue;
        quality_filters.push(filter.expression);
      }
      filters.push(quality_filters);
    }
    if (state.selectedUseFilters.length) {
      let use_filters = ["any"];
      for (let filter of state.selectedUseFilters) {
        if (filter === null) continue;
        use_filters.push(filter.expression);
      }
      filters.push(use_filters);
    }
    if (state.selectedSurveyFilters.length) {
      let survey_filters = ["all"];
      for (let filter of state.selectedSurveyFilters) {
        if (filter === null) continue;
        survey_filters.push(filter.expression);
      }
      filters.push(survey_filters);
    }
    return filters;
  },
  getAreaFilter: state => {
    return state.area;
  },
  getHeightFilter: state => {
    return state.height;
  },
  getK3Filter: state => {
    return state.k3;
  },
  getTaxFilter: state => {
    return state.tax;
  },
  getTaxOwedFilter: state => {
    return state.taxOwed;
  },
  getSelectedPropertyFilters: state => {
    return state.selectedPropertyFilters;
  },
  getSelectedQualityFilters: state => {
    return state.selectedQualityFilters;
  },
  getSelectedUseFilters: state => {
    return state.selectedUseFilters;
  },
  getSelectedSurveyFilters: state => {
    return state.selectedSurveyFilters;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};
