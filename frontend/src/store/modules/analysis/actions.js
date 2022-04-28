import axios from "axios";

let authAxios = axios.create({
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true
});

export const getAOIStats = async ({ commit }, { aoiId }) => {
  let response = await authAxios.get("/api/geodata/aoistats/", {
    params: {
      aoiId: aoiId
    }
  });
  commit("setAOIAnalysis", response.data);
};

export const getSectorStats = async ({ commit }, { sectorId }) => {
  let response = await authAxios.get("/api/geodata/sectorstats/", {
    params: {
      sectorId: sectorId
    }
  });
  commit("setSectorAnalysis", response.data);
};

export const getBlockStats = async ({ commit }, { blockId }) => {
  let response = await authAxios.post("/api/geodata/blockstats/", {
    blockId: blockId
  });
  commit("setBlockAnalysis", response.data);
};

export const getCustomBuildingAnalysis = async ({ commit }, { feature }) => {
  commit("setCustomAnalysisArea", feature);
  let response = await authAxios.post("/api/geodata/areastats/", {
    geom: feature
  });
  commit("setCustomAnalysis", response.data);
};

export const clearCustomAnalysis = ({ commit }) => {
  commit("setCustomAnalysisArea", null);
  commit("setCustomAnalysis", null);
};

export const clearAnalysisResults = ({ commit }) => {
  commit("setAOIAnalysis", null);
  commit("setSectorAnalysis", null);
  commit("setBlockAnalysis", null);
};
