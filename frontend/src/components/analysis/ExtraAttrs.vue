<template>
  <div>
    <div v-for="(attr, key, index) in attrs" :key="index">
      <dl class="row">
        <b-popover :target="'attr-info-' + index" triggers="hover" placement="top">
          {{ attr.desc }}
        </b-popover>
        <dt class="heading col-sm-8 text-uppercase text-muted">
          <b-icon-info-circle-fill :id="'attr-info-' + index" font-scale=".9" :style="iconStyle"></b-icon-info-circle-fill>
          <small>{{ attr.title }}</small>
        </dt>
        <dd class="value col-sm-4">
        {{ formatValue(attr.value) }}
        </dd>
      </dl>
    </div>
  </div>
</template>
<script>
export default {
  props: ['attrs'],
  data() {
    return {
      iconStyle: {
        color: '#919497',
        cursor: 'pointer',
        "margin-right": '5px',
      },
    }
  },
  methods: {
    formatValue(val){
      if(val === "" || val === null){
        return " -- "
      }
      else {
        return val.replaceAll("_", " ");
      }
    }
  }
}
</script>
<style scoped>

</style>
