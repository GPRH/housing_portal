<template>
  <div class="row mb-5">
    <b-col sm="4">
      <span class="heading text-uppercase text-muted">COVID Index:</span>
    </b-col>
    <b-col sm="8" class="pr-4">
      <vue-slider
        v-model="value" :data="k3Data"
       @change="setK3Filter($event)" tooltip="none"
       :marks="marks"
       ref="slider"
      >
      </vue-slider>
    </b-col>
  </div>
</template>
<script>
export default {
  props: ['result'],
  data(){
    return {
      value: 0,
      k3Data: ['3', '1.6', '1.2'],
      tooltipFormatter: "< {value}",
      marks: {
        '3': {
          label: 'all buildings',
          style: {
            width: '12px',
            height: '12px',
            display: 'block',
            // backgroundColor: '#3498db',
            backgroundColor: 'grey',
            transform: 'translate(-2px, -4px)',
            cursor: 'pointer',
          },
          labelStyle: {
            // color: '#3498db',
            color: 'grey',
            'font-weight': '500',
          }
        },
        '1.6': {
          label: 'vulnerable',
          style: {
            width: '12px',
            height: '12px',
            display: 'block',
            backgroundColor: 'orange',
            transform: 'translate(-2px, -4px)',
            cursor: 'pointer',
          },
          labelStyle: {
            color: 'orange',
            transform: 'translate(-35px, -42px)',
            'font-weight': '500',
          }
        },
        '1.2': {
          label: 'most vulnerable',
          style: {
            width: '12px',
            height: '12px',
            display: 'block',
            backgroundColor: 'red',
            transform: 'translate(-2px, -4px)',
            cursor: 'pointer',
          },
          labelStyle: {
            color: 'red',
            transform: 'translate(-85px, -2px)',
            'font-weight': '500',
          }
        },
      },
    }
  },
  computed: {
    k3Filter(){
      return this.$store.getters["filters/getK3Filter"];
    }
  },
  watch: {
    result(){
      if(this.k3Filter){
        this.value = this.k3Filter[1][2];
        this.$nextTick(() => {
          this.$refs.slider.setIndex(this.k3Data.indexOf(String(this.value)));
        });
      }
      else {
        this.value = 3;
        this.setK3Filter(this.value);
      }
    }
  },
  methods: {
    setK3Filter(value){
      let k3_filter = null;
      if(!value){
        this.$store.commit('filters/setK3Filter', k3_filter);
        this.$emit('update:covid');
        return;
      }
      let val = parseFloat(value);
      if (val < 3){
         k3_filter = ["any", ["<", ["get", "k3"], val], ["match", ["get", "k3"], "3", true, false]];
      }
      this.$store.commit('filters/setK3Filter', k3_filter);
      this.$emit('update:covid');
    }
  },
  created(){
    let _vm = this;
    _vm.$root.$on('reset-filters',() => {
      _vm.value = 3;
    });
  }
}
</script>
<style scoped>

</style>
