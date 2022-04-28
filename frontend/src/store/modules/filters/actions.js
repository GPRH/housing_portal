import axios from "axios";

let authAxios = axios.create({
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true
});

export const setFilters = (
  { commit },
  { area, building, height, tax, taxOwed, k3, property, survey }
) => {
  if (area) {
    commit("setAreaFilter", area);
  }
  if (building) {
    commit("setBuildingFilter", building);
  }
  if (height) {
    commit("setHeightFilter", height);
  }
  if (tax) {
    commit("setTaxFilter", tax);
  }
  if (taxOwed) {
    commit("setTaxOwedFilter", taxOwed);
  }
  if (k3) {
    commit("setK3Filter", k3);
  }
  if (property) {
    commit("setSelectedPropertyFilters", propFilters);
  }
  if (survey) {
    commit("setSurveyFilter", survey);
  }
};

export const clearFilters = ({ commit }) => {
  commit("setAreaFilter", null);
  commit("setBuildingFilter", null);
  commit("setHeightFilter", null);
  commit("setTaxFilter", null);
  commit("setTaxOwedFilter", null);
  commit("setK3Filter", null);
  commit("setSelectedPropertyFilters", []);
  commit("setSelectedQualityFilters", []);
  commit("setSelectedUseFilters", []);
  commit("setSelectedSurveyFilters", []);
};

export const filterAttributes = async ({ rootGetters }, { key, value }) => {
  let building_ids = [];
  let selectedAoi = rootGetters["maps/getSelectedAoi"];
  let url = `/api/geodata/building-attributes/${selectedAoi.slug}/${key}/${value}`;
  let response = await authAxios.get(url);
  if (response.status === 200) {
    building_ids = response.data;
  }
  return building_ids;
};

export const setSurveyFilterExpressions = async (
  { rootGetters, getters, dispatch },
  level
) => {
  let filters = getters["getSelectedSurveyFilters"];
  if (!filters.length) return;

  let levelBuildingIds = [];
  if (level === "custom") {
    let custom = rootGetters["analysis/getCustomAnalysis"];
    if (custom) {
      levelBuildingIds = custom["building_ids"];
    }
  }
  if (level === "sectors") {
    let sectors = rootGetters["analysis/getSectorAnalysis"];
    if (sectors) {
      levelBuildingIds = sectors["buildings"]["building_ids"];
    }
  }
  if (level === "aoi") {
    let aoi = rootGetters["analysis/getAOIAnalysis"];
    if (aoi) {
      levelBuildingIds = aoi["buildings"]["building_ids"];
    }
  }
  /* update the survey filter expression
   * to filter out the ids
   */
  for (let filter of filters) {
    let ids = await dispatch("filterAttributes", {
      key: filter.prop,
      value: filter.value
    });
    // get the intersection of the selected level ids and the filtered attr ids
    let building_ids = levelBuildingIds.filter(x => ids.includes(x));
    // if the two intersect select the intersecting ids
    if (building_ids.length) {
      filter.expression = ["match", ["id"], building_ids, true, false];
    }
    // if there is no intersection (0 results) turn off all selected level ids
    else {
      filter.expression = ["match", ["id"], levelBuildingIds, false, true];
    }
    filter.count = building_ids.length;
  }
};
