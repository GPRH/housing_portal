<template lang="html">
  <div>
    <app-main></app-main>
  </div>
</template>

<script>
import Main from "@/containers/Main.vue";
export default {
  name: "App",
  components: {
    appMain: Main
  }
};
</script>
<style>
:focus {
    outline: 0px transparent !important;
}
</style>
