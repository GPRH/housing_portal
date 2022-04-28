import { Viewer, TransitionMode } from "mapillary-js";
import axios from "axios";
import * as _ from "lodash";

const MAPILLARY_CLIENT_ID = process.env.VUE_APP_MAPILLARY_CLIENT_ID;
const MAPILLARY_USER_IDS = process.env.VUE_APP_MAPILLARY_USER_ID.split(",");

export const initMapillary = async vm => {
    vm.isInitialLoad = true;
    vm.mly = new Viewer({
        accessToken: MAPILLARY_CLIENT_ID,
        container: 'mly',
        component: {
            direction: true
        },
        transitionMode: TransitionMode.Instantaneous,
    });
    // vm.mly.setFilter(["in", "username"].concat(MAPILLARY_USER_IDS));
    let aoi = vm.$store.getters["maps/getSelectedAoi"];
    if (!vm.map.hasImage("arrow")) {
        vm.map.loadImage("/img/nav.png", function(error, image) {
            if (error) throw error;
            vm.map.addImage("arrow", image);
        });
    }
    vm.$nextTick(async() => {
        // vm.mly.setFilter(['==', 'sequenceId', aoi.sv_lat]);
        // vm.mly.moveToKey(aoi.sv_key); //depracted
        const image_ids = await getImageId([aoi.sv_lng, aoi.sv_lat]); //get image id by coordinates
        let image_id = image_ids.data[0].id;
        vm.mly.moveTo(image_id);
        vm.mly.resize();
    });

    let _vm = vm;
    window.addEventListener("resize", function() {
        _vm.mly.resize();
    });
    vm.mly.on('image', ({ image }) => {
        var lngLat = [image.lngLat.lng, image.lngLat.lat];
        updateMapillaryMarker(vm, lngLat);
        _vm.isInitialLoad = false;
        _vm.isMapReset = false;
    });
    vm.mly.on('bearing', ({ bearing }) => {
        if (vm.map.getSource("markers")) {
            vm.map.setLayoutProperty("markers", "icon-rotate", bearing);
        }
    });
    vm.mly.on('dataloading', ({ loading }) => {
        vm.$root.$emit("mapillary-data-loading", loading);
    });
    vm.$emit("mapiliary-init", vm.mly);
};

export const updateMapillaryMarker = (vm, lngLat) => {
    let aoi = vm.$store.getters["maps/getSelectedAoi"];
    if (!vm.isInitialLoad && !vm.isMapReset && vm.maximized) {
        vm.map.easeTo({ center: lngLat });
    }

    var data = {
        type: "geojson",
        data: {
            type: "Feature",
            geometry: {
                type: "Point",
                coordinates: lngLat
            },
            properties: {
                "marker-symbol": "arrow"
            }
        }
    };
    if (!vm.map.getSource("markers")) {
        vm.map.addSource("markers", data);
        vm.map.addLayer({
            id: "markers",
            type: "symbol",
            source: "markers",
            layout: {
                "icon-image": "arrow",
                "icon-size": ["interpolate", ["linear"],
                    ["zoom"], 14, 0.7, 20, 1.2
                ]
            }
        });
    } else {
        let data = {
            type: "Feature",
            geometry: {
                type: "Point",
                coordinates: lngLat
            },
            properties: {
                "marker-symbol": "arrow"
            }
        };
        vm.map.getSource("markers").setData(data);
    }
};

export const switchMapillaryAoi = async(vm) => {
    let aoi = vm.$store.getters["maps/getSelectedAoi"];
    vm.isInitialLoad = true;
    // vm.mly.moveToKey(vm.aoi.sv_key); //depracted
    // vm.mly.setFilter(['==', 'sequenceId', vm.aoi.sv_key]);
    const image_ids = await getImageId([aoi.sv_lng, aoi.sv_lat]); //get image id by coordinates
    let image_id = image_ids.data[0].id;
    vm.mly.moveTo(image_id);
};

export const setBearing = (node, bearing) => {
    if (!node.cameraType == 'spherical') { // if image is not panoramic
        // We are only interested in setting the bearing for full 360 panoramas.
        return;
    }
    var nodeBearing = node.compassAngle; // Computed node compass angle (equivalent
    // to bearing) is used by mjs when placing
    // the node in 3D space.
    var basicX = bearingToBasic(bearing, nodeBearing);
    var basicY = 0.5; // Vertical center
    var center = [basicX, basicY];
    return center;
};

/**
 * Convert a desired bearing to a basic X image coordinate for
 * a specific node bearing.
 *
 * Works only for a full 360 panorama.
 */
const bearingToBasic = (bearing, nodeBearing) => {
    // 1. Take difference of desired bearing and node bearing in degrees.
    // 2. Scale to basic coordinates.
    // 3. Add 0.5 because node bearing corresponds to the center
    //    of the image. See
    //    https://mapillary.github.io/mapillary-js/classes/viewer.html
    //    for explanation of the basic coordinate system of an image.
    var basic = (bearing - nodeBearing) / 360 + 0.5;

    // Wrap to a valid basic coordinate (on the [0, 1] interval).
    // Needed when difference between desired bearing and node
    // bearing is more than 180 degrees.
    return wrap(basic, 0, 1);
};

/**
 * Wrap a value on the interval [min, max].
 */
const wrap = (value, min, max) => {
    var interval = max - min;

    while (value > max || value < min) {
        if (value > max) {
            value = value - interval;
        } else if (value < min) {
            value = value + interval;
        }
    }

    return value;
};

//get image id by lat long
export const getImageId = async(latLong, dist = 0.0001) => {
    // let bbox_str = bbox.toString()
    latLong.push(latLong[0] + dist)
    latLong.push(latLong[1] + dist)
    latLong[0] = latLong[0] - dist
    latLong[1] = latLong[1] - dist
    const bbox = latLong.toString()
    const response = await axios.get(`https://graph.mapillary.com/images?access_token=${MAPILLARY_CLIENT_ID}&fields=id&bbox=${bbox}&limit=1`)
    return response.data
}