import { resetLayer } from "@/components/map";

export const runFilter = async (vm, level) => {
  await vm.$store.dispatch("filters/setSurveyFilterExpressions", level);
  let building_filter = getBuildingFilter(vm, level);
  vm.$store.commit("filters/setBuildingFilter", building_filter);
  let filters = vm.$store.getters["filters/getFilters"];
  vm.map.setFilter("buildings", filters);
  vm.map.setFilter("building-outlines", filters);
  applyQualityFilters(vm);
  applyUseFilters(vm);
  vm.$root.$emit("run-filters");
};

export const applyQualityFilters = vm => {
  let qualityFilters = vm.$store.getters["filters/getSelectedQualityFilters"];
  let default_color = "#0D9AD0";
  if (qualityFilters.length) {
    let thematicFilter = ["case"];
    qualityFilters.forEach(qualityFilter => {
      thematicFilter.push([
        "==",
        ["get", qualityFilter.prop],
        qualityFilter.value
      ]);
      thematicFilter.push(qualityFilter.color);
    });
    // set default color
    thematicFilter.push(default_color);
    vm.map.setPaintProperty("buildings", "fill-color", thematicFilter);
  } else {
    resetLayer(vm, "buildings");
  }
};

export const applyUseFilters = vm => {
  let useFilters = vm.$store.getters["filters/getSelectedUseFilters"];
  let default_color = "#0D9AD0";
  if (useFilters.length) {
    let thematicFilter = ["case"];
    useFilters.forEach(useFilter => {
      thematicFilter.push(["==", ["get", useFilter.prop], useFilter.value]);
      thematicFilter.push(useFilter.color);
    });
    // set default color
    thematicFilter.push(default_color);
    vm.map.setPaintProperty("buildings", "fill-color", thematicFilter);
  } else {
    // resetLayer(vm, "buildings");
  }
};

// used in search
export const filterBuildings = (vm, prop, id) => {
  let building_filter = ["match", ["get", prop], id, true, false];
  vm.$store.commit("filters/setBuildingFilter", building_filter);
  // reset area filter when selecting new block, sector or aoi
  vm.$store.commit("filters/setAreaFilter", null);
  vm.map.setFilter("buildings", building_filter);
  vm.map.setFilter("building-outlines", building_filter);
};

export const getBuildingFilter = (vm, level) => {
  let building_filter = null;
  if (level === "custom") {
    let analysis = vm.$store.getters["analysis/getCustomAnalysis"];
    if (analysis !== null) {
      let building_ids = analysis["building_ids"];
      building_filter = ["match", ["id"], building_ids, true, false];
    }
  }
  if (level === "blocks") {
    let block = vm.$store.getters["maps/getSelectedFeature"];
    if (feature !== null) {
      building_filter = [
        "match",
        ["get", "block_id"],
        block.feature.id,
        true,
        false
      ];
    }
  }
  if (level === "sectors") {
    let sector = vm.$store.getters["maps/getSelectedFeature"];
    if (sector !== null) {
      building_filter = [
        "match",
        ["get", "sector_id"],
        sector.feature.id,
        true,
        false
      ];
    }
  }
  return building_filter;
};
