<template>
  <scroll :options="scrollOptions">
    <slot name="content"></slot>
  </scroll>
</template>
<script>
export default {
  data(){
    return {
      scrollOptions: {
        scrollingThreshold: 1000,
        wheelPropagation: false,
      }
    }
  },
}
</script>
<style>
.ps {
  position: relative;
  top: 0;
  left: 0;
  border: none;
  opacity: 0.95;
  padding: 10px 5px 15px 5px;
  pointer-events: all;
  overflow: hidden;
  background: transparent;
}
@media (max-width: 768px){
  .container {
     max-height: 30vh;
  }

}
</style>
