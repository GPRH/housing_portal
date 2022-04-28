import _ from "lodash";
import mapboxgl from "mapbox-gl";
import { layers } from "./layers";
import { bbox, union, polygon, featureCollection } from "@turf/turf";
import axios from "axios";

mapboxgl.accessToken = process.env.VUE_APP_MAPBOX_ACCESS_TOKEN;
const MAPILLARY_CLIENT_ID = process.env.VUE_APP_MAPILLARY_CLIENT_ID;
const ISO_CODE = process.env.VUE_APP_PORTAL_COUNTRY_ISO_CODE;
const DEV = process.env.NODE_ENV === "development" ? true : false;

let authAxios = axios.create({
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
    withCredentials: true
});

export const setCountryMask = ({ commit }, vm) => {
    vm.map.addSource("admin-0", {
        type: "vector",
        url: "mapbox://mapbox.boundaries-adm0-v3"
    });
    vm.map.addLayer({
            id: "admin-0-fill",
            type: "fill",
            source: "admin-0",
            "source-layer": "boundaries_admin_0",
            paint: {
                "fill-color": [
                    "match", ["get", "iso_3166_1"],
                    `${ISO_CODE}`,
                    "transparent",
                    "#787b8c"
                ],
                "fill-opacity": 0.3
            }
        },
        "waterway-label"
    );
};

export const loadAOIS = async({ commit }) => {
    let response = await authAxios.get("/api/geodata/aoinames/");
    commit("setAois", response.data);
};

export const setBaseLayer = ({ commit }, { map, baseLayer }) => {
    if (baseLayer.name === "Imagery") {
        map.setMaxZoom(14);
    } else {
        map.setMaxZoom(22);
    }
    map.setStyle(baseLayer.style, { diff: false });
    commit("setBaseLayer", baseLayer);
};

// load layers
export const loadLayers = async({ state, dispatch, commit, getters }, { vm }) => {
    commit("clearLayers");
    let aoi = state.selectedAOI;
    let config = getters["getAoiConfig"];
    for (let l in layers) {
        let layer = layers[l];

        // check if the layer should be loaded for this aoi
        if (!layer.aois.includes(aoi.slug)) {
            continue;
        }
        let lyr = JSON.parse(JSON.stringify(layer));
        if (lyr.source.type === "vector") {
            // add the aoi id to the tiles url and aoi id to filter
            let url = lyr.source.tiles[0];
            url = url.split("{id}").join(aoi.id);
            lyr.source.tiles[0] = url;
        }
        if (lyr.id === "drone-cover") {
            lyr.source.tiles[0] = lyr.source.tiles[0].replace("{aoi}", aoi.slug);
        }
        if (lyr.id === "sector-labels") {
            lyr.source.data = lyr.source.data.replace("{aoi}", aoi.name);
        }

        if (!vm.map.getLayer(lyr)) {
            lyr.minzoom = config[lyr.id].minZoom;
            lyr.maxzoom = config[lyr.id].maxZoom;
            vm.map.addLayer(lyr);
        }
        // make sure mapillary marker stays on top.
        if (vm.map.getLayer("markers")) {
            vm.map.moveLayer(layer.id, "markers");
        }

        if (!lyr.checked) {
            vm.map.setLayoutProperty(lyr.id, "visibility", "none");
        }
        commit("addLayer", lyr);
    }
};

export const setDisplayLayers = ({ commit }, layers) => {
    commit("setDisplayLayers", layers);
};

export const removeDisplayLayer = ({ commit, getters }, layer) => {};

export const setBounds = ({ commit }, payload) => {
    commit("setBounds", payload);
};

export const clearLayers = async({ commit, dispatch, state }, { vm }) => {
    let layers = state.layers;
    for (let l in layers) {
        let layer = layers[l];
        dispatch("removeLayer", { vm: vm, layer: layer });
    }
    commit("clearLayers");
    commit("setDisplayLayers", []);
};

export const removeLayer = ({ commit }, { vm, layer }) => {
    if (vm.map.getLayer(layer.id)) {
        vm.map.removeLayer(layer.id);
    }
    if (layer.source === "composite") {
        // ignore layers with sources derived from mapbox baselayer
        return;
    }
    if (vm.map.getSource(layer.id)) {
        vm.map.removeSource(layer.id);
    }
    commit("removeLayer", layer);
};

export const selectFeature = async({ commit, dispatch, state, getters }, { vm, feature, layer, preserveZoom }) => {
    let selectedFeature = state.selectedFeature;
    if (selectedFeature !== null) {
        // reset selected state on existing selected feature
        vm.map.setFeatureState({
            source: selectedFeature.layer,
            id: selectedFeature.feature.id,
            sourceLayer: "default"
        }, { selected: false, hover: false });
        // deselect building outlines
        vm.map.setFeatureState({
            source: "building-outlines",
            id: selectedFeature.feature.id,
            sourceLayer: "default"
        }, { selected: false, hover: false });
    }
    // set selected feature state
    vm.map.setFeatureState({ source: layer, id: feature.id, sourceLayer: "default" }, { selected: true, hover: false });
    if (layer === "buildings") {
        // select building-outlines
        vm.map.setFeatureState({ source: "building-outlines", id: feature.id, sourceLayer: "default" }, { selected: true, hover: false });
        let building = await getBuildingDetail(feature.id);
        let geom = Object.assign({}, feature.geometry);
        feature = Object.assign({}, feature);
        feature.geometry = geom;
        feature.properties = building.properties;
        feature.properties.images = building.properties.images;
    }
    // store the selected feature
    commit("selectFeature", { feature: feature, layer: layer });

    // fit map to selected feature extent
    let extent = null;
    if (layer === "aoi") {
        extent = vm.$store.getters["analysis/getAOIAnalysis"].extent;
    } else if (layer === "sectors") {
        extent = vm.$store.getters["analysis/getSectorAnalysis"].extent;
    } else {
        extent = bbox(feature.geometry);
    }
    var bounds = new mapboxgl.LngLatBounds(extent);
    let config = getters["getAoiConfig"];
    var maxZoom = layer === "sectors" ? config["sectors"].maxZoom - 0.1 : 20;
    if ((layer === "aoi" || layer === "sectors") && !preserveZoom) {
        vm.map.fitBounds(bounds, {
            padding: { top: 60, right: 0, left: 220, bottom: 20 },
            linear: true,
            maxZoom: maxZoom
        });
    }
    vm.$root.$emit("feature-selected");
};

export const clearSelectedFeature = ({ commit, state, dispatch }, { vm }) => {
    let selectedFeature = state.selectedFeature;
    if (selectedFeature !== null) {
        if (vm.map.getSource(selectedFeature.layer)) {
            vm.map.setFeatureState({
                source: selectedFeature.layer,
                id: selectedFeature.feature.id,
                sourceLayer: "default"
            }, { selected: false, hover: false });
            if (selectedFeature.layer === "buildings") {
                //deselect building-outlines
                vm.map.setFeatureState({
                    source: "building-outlines",
                    id: selectedFeature.feature.id,
                    sourceLayer: "default"
                }, { selected: false, hover: false });
            }
        }
    }
    if (vm.map.getLayer("buildings")) {
        vm.map.setFilter("buildings", null);
    }
    if (vm.map.getLayer("building-outlines")) {
        vm.map.setFilter("building-outlines", null);
    }
    commit("selectFeature", null);
    dispatch("analysis/clearAnalysisResults", null, { root: true });
    vm.$root.$emit("feature-deselected");
};

export const getBuildingDetail = async id => {
    let response = await authAxios.get("/api/geodata/buildings/" + id + "/");
    return response.data;
};

export const search = async({ commit, getters }, { query, proximity }) => {
    let v4 = new RegExp(
        /^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i
    );
    let geohash = new RegExp(/^[a-z0-9]{10}$/i);
    let search_param = "";
    if (query.match(v4)) {
        search_param = "uid";
    } else if (query.match(geohash)) {
        search_param = "geohash";
    } else {
        search_param = "address";
    }
    let results = { mapbox: [], local: [] };
    let aoi = getters["getSelectedAoi"];
    if (search_param === "address") {
        let url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?access_token=${mapboxgl.accessToken}&bbox=${aoi.extent}&types=postcode,district,place,locality,neighborhood,address,poi&proximity=${proximity.lng},${proximity.lat}`;
        let mapbox = await axios.get(url, { crossDomain: true });
        results["mapbox"] = mapbox.data.features;
    }
    let local = await authAxios.get(
        "/api/geodata/buildings/?" + search_param + "=" + query + "&aoi=" + aoi.name
    );
    results["local"] = local.data.features;
    return results;
};

// not used at the moment but might be useful later...
// will not work on V4
export const getMapillaryImageLookAt = async({ commit }, latlng) => {
    let lat = latlng[1];
    let lng = latlng[0];
    let imageUrl = `https://a.mapillary.com/v3/images?client_id=${MAPILLARY_CLIENT_ID}&closeto=${lng},${lat}&radius=50&lookat=${lng},${lat}`;
    let response = await axios.get(imageUrl);
    return response;
};