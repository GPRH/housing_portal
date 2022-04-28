<template>
  <div class="p-1 container">
    <span class="info" @click="$emit('passport-info-click')">
      <em>Passport information </em>
      <b-icon-info-circle-fill font-scale="1.1" :style="iconStyle"  title="Passport information"></b-icon-info-circle-fill>
    </span>
  </div>
</template>
<script>
export default {
  data(){
    return {
      iconStyle: {
        color: 'darkgrey',
        cursor: 'pointer',
      }
    }
  }
}
</script>
<style scoped>
.info {
  /* border-top: 1px solid lightgrey; */
  opacity: 0.95;
  cursor: pointer;
}
</style>
