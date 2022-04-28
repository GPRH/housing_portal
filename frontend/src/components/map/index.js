import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
// import "mapillary-js/dist/mapillary.min.css";
import "mapillary-js/dist/mapillary.css";
import "@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import { Viewer } from "mapillary-js";
import { eventHandlers, selectAoi } from "@/components/map/events";

const DEV_ENV = process.env.NODE_ENV === "development" ? true : false;

export const initMap = async vm => {
    let baseLayers = vm.$store.state.maps.baseLayers;
    mapboxgl.accessToken = process.env.VUE_APP_MAPBOX_ACCESS_TOKEN;
    let config = vm.config;

    // check for selected layer
    let selectedBaseLayer = vm.$store.getters["maps/getSelectedBaseLayer"];
    let defaultBounds = vm.$store.getters["maps/getDefaultBounds"];
    let defaultCenter = vm.$store.getters["maps/getDefaultCenter"];
    let style = selectedBaseLayer.style;

    var map = new mapboxgl.Map({
        container: "map", // HTML container id
        center: defaultCenter,
        style: style,
        zoom: config.map.initialZoom,
        minZoom: config.map.minZoom,
        maxZoom: config.map.maxZoom
    });
    vm.map = map;
    map.on("load", e => {
        vm.$store.dispatch("maps/setCountryMask", vm);
    });
};

export const addControls = (vm, map) => {
    let defaultBounds = vm.$store.getters["maps/getDefaultBounds"];
    var nav = new mapboxgl.NavigationControl();
    map.addControl(nav, "bottom-right");
};

export const loadAOILayers = async vm => {
    vm.map.setMaxBounds(null);
    vm.isInitialLoad = true;
    await vm.$store.dispatch("maps/clearLayers", { vm: vm });
    vm.$store.dispatch("maps/clearSelectedFeature", { vm: vm });
    await vm.$store.dispatch("maps/setDisplayLayers", []);
    await vm.$store.dispatch("maps/loadLayers", { vm: vm });
    let aoi = vm.$store.getters["maps/getSelectedAoi"];
    let config = vm.$store.getters["maps/getAoiConfig"];
    let bounds = new mapboxgl.LngLatBounds(aoi.extent);
    vm.map.on("sourcedata", function(e) {
        if (e.sourceId === "aoi") {
            if (
                vm.map.getSource("aoi") &&
                vm.map.isSourceLoaded("aoi") &&
                vm.isInitialLoad
            ) {
                var features = vm.map.queryRenderedFeatures({
                    layers: ["aoi"]
                });
                if (features.length) {
                    selectAoi(vm, features[0]);
                    vm.isInitialLoad = false;
                }
            }
        }
        if (e.sourceId === "buildings" && e.isSourceLoaded) {
            vm.$root.$emit("buildings-loaded");
        }
    });
    vm.map.fitBounds(
        bounds, {
            padding: { top: 60, right: 0, left: 220, bottom: 20 },
            maxZoom: config.aoi.minZoom
        }, { source: "selectAoi" }
    );
};

export const addEventHandlers = vm => {
    eventHandlers(vm);
};

export const resetLayers = vm => {
    updateLayerVisibility(vm);
    updateDisplayLayers(vm);
};

// layer utilities
export const resetLayer = (vm, layerId) => {
    let map = vm.map;
    let layers = vm.$store.getters["maps/getLayers"];
    for (let layer of layers) {
        if (layer.id == layerId) {
            if (layer.type === "fill") {
                let fill = layer.paint["fill-color"];
                map.setPaintProperty(layerId, "fill-color", fill);
            }
            if (layer.type === "line") {
                let lineColor = layer.paint["line-color"];
                map.setPaintProperty(layerId, "line-color", lineColor);
            }
        }
    }
};

export const resetBuildings = vm => {
    resetLayer(vm, "buildings");
    resetLayer(vm, "building-outlines");
};

export const updateDisplayLayers = vm => {
    let zoom = vm.map.getZoom();
    let layers = vm.$store.getters["maps/getLayers"];
    let displayLayers = _.filter(layers, layer => {
        return zoom >= layer.minzoom && zoom < layer.maxzoom && layer.switcher;
    });
    vm.$store.dispatch("maps/setDisplayLayers", displayLayers);
};

export const updateLayerVisibility = vm => {
    let zoom = vm.map.getZoom();
    let config = vm.$store.getters["maps/getAoiConfig"];
    let selectedFeature = vm.$store.getters["maps/getSelectedFeature"];
    if (selectedFeature && selectedFeature.layer === "sectors") {
        vm.map.setLayoutProperty("buildings", "visibility", "visible");
        vm.map.setLayoutProperty("building-outlines", "visibility", "visible");
        checkBuildingLayer(vm, true);
    }
    if (selectedFeature && selectedFeature.layer === "aoi") {
        vm.map.setLayoutProperty("buildings", "visibility", "visible");
        vm.map.setLayoutProperty("building-outlines", "visibility", "visible");
        checkBuildingLayer(vm, true);
    }
};

const checkBuildingLayer = (vm, visible) => {
    let layers = vm.$store.getters["maps/getLayers"];
    for (let layer of layers) {
        if (layer.id === "buildings" || layer.id === "building-outlines") {
            layer.checked = visible;
        }
    }
};