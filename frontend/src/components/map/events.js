import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { center, bbox } from "@turf/turf";
import numeral from "numeral";
import { runFilter, updateCustomAreaFilters } from "@/components/filters";

import {
  resetLayers,
  resetLayer,
  resetBuildings,
  updateLayerVisibility,
  updateDisplayLayers
} from "@/components/map";

export const eventHandlers = vm => {
  let aoi = vm.$store.getters["maps/getSelectedAoi"];

  addClickEvents(vm, aoi);
  addZoomEvents(vm);
  addHighlightEvents(vm, aoi);
  addHoverInfoEvents(vm);
  addDataEvents(vm);
  addDrawEvents(vm);
  addFeatureEvents(vm);
  addMapResetEvents(vm);
  addLogoutEvents(vm);
};

export const addClickEvents = (vm, aoi) => {
  let map = vm.map;

  map.on("click", e => {
    let isDrawing = vm.isDrawing;
    var f = map.queryRenderedFeatures(e.point, {
      layers: ["buildings"]
    });
    if (f.length && !isDrawing) {
      vm.$store.dispatch("filters/clearFilters");
      map.setFilter("buildings", null);
      map.setFilter("building-outlines", null);
      resetBuildings(vm);
      var feature = f[0];
      selectBuilding(vm, feature);
      return;
    }
    f = map.queryRenderedFeatures(e.point, { layers: ["sectors"] });
    if (f.length && !isDrawing) {
      var feature = f[0];
      selectSector(vm, feature);
      return;
    }
    f = map.queryRenderedFeatures(e.point, { layers: ["aoi"] });
    if (f.length && !isDrawing) {
      var feature = f[0];
      selectAoi(vm, feature);
      return;
    }
    if (!isDrawing) {
      let selectedFeature = vm.$store.getters["maps/getSelectedFeature"];
      if (selectedFeature.layer !== "aoi") {
        vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
        resetBuildings(vm);
        let aoiFeature = vm.$store.getters["maps/getSelectedAoi"].feature;
        selectAoi(vm, aoiFeature.feature, true);
      }
    }
  });
};

export const selectAoi = async (vm, feature, preserveZoom) => {
  // vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
  var id = feature.id;
  vm.$root.$emit("analysis-data-loading", true);
  await vm.$store.dispatch("analysis/getAOIStats", { aoiId: id });
  vm.$store.dispatch("maps/selectFeature", {
    vm: vm,
    feature: feature,
    layer: "aoi",
    preserveZoom: preserveZoom
  });
  vm.$store.dispatch("filters/clearFilters");
  resetBuildings(vm);
  vm.$root.$emit("analysis-data-loading", false);
};

export const selectSector = async (vm, feature) => {
  var id = feature.id;
  vm.$root.$emit("analysis-data-loading", true);
  await vm.$store.dispatch("analysis/getSectorStats", { sectorId: id });
  vm.$store.dispatch("maps/selectFeature", {
    vm: vm,
    feature: feature,
    layer: "sectors"
  });
  // filter by sector
  runFilter(vm, "sectors");
  vm.$root.$emit("analysis-data-loading", false);
};

export const selectBuilding = async (vm, feature) => {
  var id = feature.id;
  // vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
  await vm.$store.dispatch("maps/selectFeature", {
    vm: vm,
    feature: feature,
    layer: "buildings"
  });
  vm.$store.dispatch("filters/clearFilters");
  resetBuildings(vm);
};

export const addHighlightEvents = (vm, aoi) => {
  let map = vm.map;
  let hoverFeature = null;

  map.on("mousemove", function(e) {
    let isDrawing = vm.isDrawing;
    // let layers = ["buildings", "blocks", "sectors", "aoi"];
    let layers = ["buildings", "sectors", "aoi", "greenspaces"];
    let f = map.queryRenderedFeatures(e.point, {
      layers: layers
    });
    map.getCanvas().style.cursor = f.length && !isDrawing ? "pointer" : "";
    if (f.length && !isDrawing) {
      var feature = f[0];
      if (hoverFeature !== null) {
        map.setFeatureState(
          {
            source: hoverFeature.source,
            id: hoverFeature.id,
            sourceLayer: "default"
          },
          { hover: false }
        );
      }
      hoverFeature = feature;
      map.setFeatureState(
        {
          source: hoverFeature.source,
          id: hoverFeature.id,
          sourceLayer: "default"
        },
        { hover: true }
      );
    } else {
      if (hoverFeature !== null) {
        map.setFeatureState(
          {
            source: hoverFeature.source,
            id: hoverFeature.id,
            sourceLayer: "default"
          },
          { hover: false }
        );
      }
    }
  });

  map.on("mouseleave", function() {
    if (hoverFeature !== null) {
      map.setFeatureState(
        {
          source: hoverFeature.source,
          id: hoverFeature.id,
          sourceLayer: "default"
        },
        { hover: false }
      );
    }
    hoverFeature = null;
  });
};

export const addZoomEvents = vm => {
  let map = vm.map;
  map.on("moveend", e => {
    vm.$store.dispatch("maps/setBounds", e.target.getBounds());
  });

  map.on("zoomend", e => {
    updateDisplayLayers(vm);
    updateLayerVisibility(vm);
    if (!vm.map.isSwitching) {
      let config = vm.$store.getters["maps/getAoiConfig"];
      vm.map.setMinZoom(config.aoi.minZoom);
    }
    if (e.source && e.source === "selectAoi") {
      map.setMaxBounds(e.target.getBounds());
    }
  });
};

export const addHoverInfoEvents = vm => {
  let map = vm.map;
  const layers = ["aoi", "sectors", "greenspaces", "buildings"];
  map.on("mousemove", e => {
    let f = map.queryRenderedFeatures(e.point, {
      layers: layers
    });
    if (f.length) {
      vm.$root.$emit("hover-info-show", f[0]);
    }
  });

  for (let layer of layers) {
    map.on("mouseleave", layer, () => {
      map.getCanvas().style.cursor = "";
      vm.$root.$emit("hover-info-close");
    });
  }
};

// draw events
export const addDrawEvents = vm => {
  let map = vm.map;

  map.on("draw.create", async e => {
    vm.$root.$emit("analysis-data-loading", true);
    var feature = e.features[0].geometry;
    await vm.$store.dispatch("analysis/getCustomBuildingAnalysis", {
      feature: feature
    });
    runFilter(vm, "custom");
    var extent = bbox(feature);
    var bounds = new mapboxgl.LngLatBounds(extent);
    vm.map.fitBounds(bounds, {
      padding: { top: 60, right: 0, left: 220, bottom: 20 },
      linear: true
    });
    vm.$root.$emit("analysis-data-loading", false);
  });

  map.on("draw.update", async e => {
    vm.$root.$emit("analysis-data-loading", true);
    var feature = e.features[0].geometry;
    await vm.$store.dispatch("analysis/getCustomBuildingAnalysis", {
      feature: feature
    });
    runFilter(vm, "custom");
    var extent = bbox(feature);
    var bounds = new mapboxgl.LngLatBounds(extent);
    vm.map.fitBounds(bounds, {
      padding: { top: 70, right: 0, left: 220, bottom: 30 },
      linear: true
    });
    vm.$root.$emit("analysis-data-loading", false);
  });

  vm.$root.$on("draw-stopped", () => {
    resetLayers(vm);
  });
};

export const addFeatureEvents = vm => {
  let map = vm.map;

  vm.$root.$on("feature-selected", () => {
    updateLayerVisibility(vm);
    updateDisplayLayers(vm);
  });
  vm.$root.$on("feature-deselected", () => {
    let zoom = map.getZoom();
    // if (zoom < 18) {
    //   if (map.getLayer("buildings")) {
    //     map.setLayoutProperty("buildings", "visibility", "none");
    //   }
    // }
  });
};

export const addDataEvents = vm => {
  let map = vm.map;
  map.on("data", data => {});
  map.on("dataloading", data => {});
};

export const addMapResetEvents = vm => {
  vm.map.on("moveend", function(e) {
    if (e.source === "reset-map") {
      var features = vm.map.queryRenderedFeatures({
        layers: ["aoi"]
      });
      if (features.length) {
        selectAoi(vm, features[0]);
      }
    }
  });
};

export const addLogoutEvents = vm => {
  vm.$root.$on("before-logout", () => {
    vm.$store.dispatch("maps/setDisplayLayers", []);
    vm.$store.dispatch("analysis/clearAnalysisResults");
    vm.$store.dispatch("analysis/clearCustomAnalysis");
    vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
  });
  vm.$root.$on("logout", () => {
    vm.$store.dispatch("maps/setDisplayLayers", []);
    vm.$store.dispatch("analysis/clearAnalysisResults");
    vm.$store.dispatch("analysis/clearCustomAnalysis");
    vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
    vm.$store.commit("maps/setSelectedAoi", null);
  });
};
