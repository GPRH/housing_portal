<template>
  <b-container id="splash" fluid class="d-flex align-items-center justify-content-center">
    <b-row>
      <b-col>
        <div class="splash-title text-uppercase text-light">There's no place like home!</div>
        <div class="splash-subtitle text-light">
          A Housing Portal to <span class="hl">Find</span>, <span class="hl">Build</span>
          and <span class="hl">Strengthen</span> Homes
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
export default {
  computed:{
    loggedIn(){
      return this.$store.getters['isLoggedIn']
    }
  }
}
</script>
<style scoped>
#splash {
  position: absolute;
  left: 0;
  right: 0;
  font-family: 'Roboto', sans-serif;
  font-size: 1vw;
  background-color: transparent;
  z-index: 400;
  top: 45%;
  pointer-events: none;
}
.splash-title {
  font-size: 3.3em;
}
.splash-subtitle {
  font-size: 2em;
}
.hl {
  color: #EAD306;
  font-weight: 500;
}
</style>
