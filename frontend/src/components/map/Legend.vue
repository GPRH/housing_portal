<template>
  <div class="d-flex d-inline-block ml-2">
    <svg v-if="legend.type === 'circle'" width="18px" height="18px">
      <circle cx="9" cy="9" r="9" :fill="legend.fill" :opacity="legend.opacity"></circle>
    </svg>
    <svg v-if="legend.type === 'fill'" width="18px" height="18px">
      <rect width="18" height="18" :fill="legend.fill" :stroke="legend.outline" :opacity="legend.opacity"></rect>
    </svg>
    <svg v-if="legend.type === 'line'" width="18px" height="18px">
      <line
        x1="0"
        y1="10"
        x2="18"
        y2="10"
        :style="'stroke:' + legend.outline + ';stroke-width:' + legend.width"
      ></line>
    </svg>
    <svg v-if="legend.type === 'image'" width="18px" height="18px">
       <image href="img/drone.png" height="18" width="18" :stroke="legend.outline"/>
    </svg>
  </div>
</template>
<script>
export default {
  props: ["legend"]
};
</script>
