import * as actions from "./actions";
import { aoi_tax_fields } from "./taxes";
import { aoi_covid_fields } from "./covid";
import { aoi_survey_fields } from "./survey";
import { display_infrastructure_field } from "./infrastructure";
import { include_attr_config } from "./attr_config";

const state = {
  sectorAnalysis: null,
  blockAnalysis: null,
  aoiAnalysis: null,
  customArea: null,
  customAnalysis: null,
  aoiTaxFields: aoi_tax_fields,
  aoiCovidFields: aoi_covid_fields,
  aoiSurveyFields: aoi_survey_fields,
  aoiIncludeAttrs: include_attr_config,
  aoiInfrastructureField: display_infrastructure_field
};

const mutations = {
  setBlockAnalysis(state, blockAnalysis) {
    state.blockAnalysis = blockAnalysis;
  },
  setSectorAnalysis(state, sectorAnalysis) {
    state.sectorAnalysis = sectorAnalysis;
  },
  setAOIAnalysis(state, aoiAnalysis) {
    state.aoiAnalysis = aoiAnalysis;
  },
  setCustomAnalysisArea(state, feature) {
    state.customArea = feature;
  },
  setCustomAnalysis(state, customAnalysis) {
    state.customAnalysis = customAnalysis;
  }
};

const getters = {
  getBlockAnalysis: state => {
    return state.blockAnalysis;
  },
  getSectorAnalysis: state => {
    return state.sectorAnalysis;
  },
  getAOIAnalysis: state => {
    return state.aoiAnalysis;
  },
  getCustomAnalysis: state => {
    return state.customAnalysis;
  },
  getAoiTaxFields: state => {
    return state.aoiTaxFields;
  },
  getAoiCovidFields: state => {
    return state.aoiCovidFields;
  },
  getAoiSurveyFields: state => {
    return state.aoiSurveyFields;
  },
  getAoiIncludeAttrs: state => {
    return state.aoiIncludeAttrs;
  },
  getAoiInfrastructureField: state => {
    return state.aoiInfrastructureField;
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
};
