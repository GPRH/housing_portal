<template>
  <div id="mly" v-show="show" :class="maximized ? 'maximized' : 'minimized'">
    <app-switcher :map="map" :maximized="maximized"></app-switcher>
    <app-indicator :maximized="maximized"></app-indicator>
    <app-nodata :nodata="nodata" :maximized="maximized"></app-nodata>
  </div>
</template>
<script>
import Switcher from "@/components/mapillary/Switcher";
import MapilliaryIndcator from "@/components/mapillary/MapillaryIndicator";
import MapillaryNoData from "@/components/mapillary/MapillaryNoData";
import {
  initMapillary,
  switchMapillaryAoi,
  updateMapillaryMarker,
  getImageKey,
  setBearing,
  getImageId,
} from "@/components/mapillary";
import { center, bearing, point, lineString, bbox } from "@turf/turf";
import axios from "axios";
export default {
  props: ["map"],
  data() {
    return {
      maximized: false,
      mly: null,
      show: false,
      isInitialLoad: false,
      isMapReset: false,
      nodata: false,
    };
  },
  components: {
    appSwitcher: Switcher,
    appIndicator: MapilliaryIndcator,
    appNodata: MapillaryNoData,
  },
  computed: {
    aoi() {
      return this.$store.getters["maps/getSelectedAoi"];
    },
    style() {
      if (this.maximized) {
        return {
          width: "100%",
          left: 0,
          bottom: 0,
          height: "calc(100vh)",
          position: "absolute",
          "border-radius": "0px",
        };
      }
    },
  },
  created() {
    let _vm = this;
    this.$root.$on("resize-map", ({ show }) => {
      _vm.$nextTick(() => {
        _vm.mly.resize();
      });
    });
    this.$root.$on("toggle-mapillary", () => {
      _vm.maximized = !_vm.maximized;
      _vm.nodata = false;
      _vm.$nextTick(() => {
        _vm.mly.resize();
        if (_vm.maximized && _vm.mly) {
          _vm.mly.getPosition().then((pos) => {
            _vm.map.easeTo({ center: [pos.lng, pos.lat] });
          });
        }
      });
    });
    _vm.$root.$on("address-selected", async (latlng) => {
      const image_ids = await getImageId([latlng[0], latlng[1]]); //get image id by coordinates
      let image_id = image_ids.data[0].id;
      _vm.mly.moveTo(image_id);
    });
    _vm.$root.$on("feature-selected", async () => {
      _vm.nodata = false;
      // remove any warnings
      _vm.$root.$emit("mapillary-warning", { show: false, coords: null });
      let selectedFeature = _vm.$store.getters["maps/getSelectedFeature"];
      if (selectedFeature && selectedFeature.layer === "buildings") {
        let latlng = center(selectedFeature.feature.geometry).geometry
          .coordinates;
        let extent = bbox(selectedFeature.feature.geometry);
        let images = selectedFeature.feature.properties.images;
        if (images.length) {
          let image = images[0];
          console.log(image);
          const image_ids = await getImageId([image.lon, image.lat]); //get image id by coordinates

          if (!image_ids.data.length) {
            //if there is no image in the given point
            _vm.nodata = true;
            return;
          }

          let image_id = image_ids.data[0].id;
          _vm.mly
            .moveTo(image_id)
            .then((node) => {
              console.log(node);
              let imageLonLat = point([node.lngLat.lng, node.lngLat.lat]);
              let buildingLonLat = point([latlng[0], latlng[1]]);
              let line = lineString(
                [
                  imageLonLat.geometry.coordinates,
                  buildingLonLat.geometry.coordinates,
                ],
                { name: "connecting line" }
              );
              let extent = bbox(line);
              let fullPano = node.cameraType == "spherical";
              if (fullPano) {
                let _center = setBearing(node, image.angle);
                if (_center) {
                  _vm.mly.setCenter(_center);
                  _vm.map.setLayoutProperty(
                    "markers",
                    "icon-rotate",
                    image.angle
                  );
                  _vm.map.fitBounds(extent, {
                    padding: { top: 60, right: 120, left: 120, bottom: 20 },
                    linear: true,
                    maxZoom: 19,
                  });
                }
              } else {
                _vm.$root.$emit("mapillary-warning", {
                  show: true,
                  coords: imageLonLat.geometry.coordinates,
                });
                _vm.map.fitBounds(extent, {
                  padding: { top: 160, right: 0, left: 0, bottom: 120 },
                  maxZoom: 19,
                });
              }
            })
            .catch((error) => {
              if (error.name === "AbortMapillaryError") {
                console.warn("Aborting mapillary request.");
              }
              if (error.message.startsWith("No image found")) {
                console.warn("No mapillary image found");
                _vm.nodata = true;
              }
            });
        } else {
          console.log("no building image");
          // we don't have a building image so move close to the building centroid lat long
          _vm.nodata = false;
          const image_ids = await getImageId([latlng[0], latlng[1]], 0.0002); //get image id by coordinates

          if (!image_ids.data.length) {
            //if there is no image in the given point
            _vm.nodata = true;
            return;
          }

          let image_id = image_ids.data[0].id;
          _vm.mly
            .moveTo(image_id)
            .then((node) => {
              let imageLonLat = point([node.lngLat.lng, node.lngLat.lat]);
              this.coords = imageLonLat.geometry.coordinates;
              let buildingLonLat = point([latlng[0], latlng[1]]);
              let angle = bearing(imageLonLat, buildingLonLat);
              let line = lineString(
                [
                  imageLonLat.geometry.coordinates,
                  buildingLonLat.geometry.coordinates,
                ],
                { name: "connecting line" }
              );
              let extent = bbox(line);
              let fullPano = node.cameraType == "spherical";
              if (fullPano) {
                let center = setBearing(node, angle);
                if (center) {
                  _vm.mly.setCenter(center);
                  _vm.map.setLayoutProperty("markers", "icon-rotate", angle);
                  _vm.map.fitBounds(extent, {
                    padding: { top: 160, right: 0, left: 0, bottom: 120 },
                    maxZoom: 19,
                  });
                }
              } else {
                _vm.$root.$emit("mapillary-warning", {
                  show: true,
                  coords: imageLonLat.geometry.coordinates,
                });
                _vm.map.setLayoutProperty("markers", "icon-rotate", angle);
                _vm.map.fitBounds(extent, {
                  padding: { top: 160, right: 0, left: 0, bottom: 120 },
                  maxZoom: 19,
                });
              }
            })
            .catch((error) => {
              if (error.message.startsWith("No image found")) {
                console.warn("No image found");
                _vm.nodata = true;
                _vm.map.fitBounds(extent, {
                  padding: { top: 160, right: 0, left: 0, bottom: 120 },
                  maxZoom: 19,
                });
              }
            });
        }
      }
    });
    _vm.$root.$on("aoi-selected", () => {
      if (!_vm.mly) {
        _vm.show = true;
        _vm.isInitalLoad = true;
        initMapillary(_vm);
      } else {
        _vm.isInitalLoad = true;
        switchMapillaryAoi(_vm);
      }
    });
    _vm.$root.$on("reset-map", async() => {
      let aoi = _vm.$store.getters["maps/getSelectedAoi"];
      _vm.isMapReset = true;
      // _vm.mly.moveToKey(aoi.sv_key); //depracted
      // _vm.mly.setFilter(["==", "sequenceId", aoi.sv_key]);
      const image_ids = await getImageId([aoi.sv_lng, aoi.sv_lat]); //get image id by coordinates
      let image_id = image_ids.data[0].id;
      _vm.mly.moveTo(image_id);
    });
  },
};
</script>
<style>
#mly.maximized {
  position: absolute;
  left: 0;
  top: 0px;
  width: 100vw;
  height: 100vh;
  border-radius: 0px;
  overflow: hidden;
}

#mly.minimized {
  position: absolute;
  top: calc(100vh - 36vh);
  left: 22px;
  width: 320px;
  height: 240px;
  z-index: 1200;
  -webkit-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 3px 3px 5px 0px rgba(0, 0, 0, 0.75);
}

@media (max-width: 768px) {
  #mly.minimized {
    position: absolute;
    left: 22px;
    border-radius: 4px;
    border: 1px solid lightgrey;
  }
}

/* #mly.maximized > div.mapillary-js-dom > div.domRenderer > div.SequenceContainer {
  top: 50px;
} */

div.mapillary-js-dom > div.domRenderer > div.SequenceContainer {
  display: none;
}

#mly.minimized .mapillary-js-canvas {
  /* border-radius: 8px; */
}
</style>
