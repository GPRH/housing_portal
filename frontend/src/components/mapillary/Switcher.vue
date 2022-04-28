<template>
  <div id="switcher" v-if="!maximized" @click="toggleMapillary()">
    <b-icon-arrows-fullscreen id="icon" scale=1.2  aria-hidden="true"></b-icon-arrows-fullscreen>
  </div>
</template>
<script>
export default {
  props: ["map", "maximized"],
  data() {
    return {
      maximizeIcon: ["fas", "expand"],
    };
  },
  methods: {
    toggleMapillary() {
      this.$root.$emit("toggle-mapillary");
    }
  }
};
</script>
<style scoped>
#icon {
  padding: .5em;
}
#switcher {
  position: absolute;
  top: 5px;
  right: 10px;
  z-index: 999;
  background: white;
  cursor: pointer;
  color: black;
  border-radius: 4px;
  opacity: 1;
  font-size: 15px;
  height: 30px;
  width: 30px;
  line-height: 1;
  z-index: 1400 !important;
  pointer-events: all;
}
#switcher:hover {
  background-color: whitesmoke;
  line-height: 1;
}
</style>
