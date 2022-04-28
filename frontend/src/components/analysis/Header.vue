<template>
  <div class="header d-flex align-items-center pl-2">
    <span id="title" class="text-uppercase text-light font-weight-bold">
      <slot name="title">Passport</slot>
    </span>
    <!-- <span id="closeBtn" class="text-light float-right" @click="close()">
      <b-icon-x-circle title="Close Passport"></b-icon-x-circle>
    </span> -->
  </div>
</template>
<script>
export default {
  methods: {
    close() {
      this.$emit("close");
    }
  }
}
</script>
<style scoped>
#title {
  font-size: 1.2em;
  padding: .4em;
  /* float: right !important; */
  width: 100%;
}
#closeBtn {
  font-size: 1.1em;
  font-weight: 600;
  padding: .4em .4em .4em .4em;
  cursor: pointer;
}
.header {
  background-color:#C63D39;
  padding: .2em;
}
</style>
