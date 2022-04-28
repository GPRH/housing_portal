<template>
  <div>
    <slot name="header"></slot>
    <app-scroll>
      <template v-slot:content>
        <b-collapse id="analysis-panel" visible>
          <div id="attrs" class="p-3">
            <dl class="row">
              <dt class="col-sm-6 text-uppercase text-muted">
                <small>Address:</small>
              </dt>
              <dd class="col-sm-6">{{ selectedFeature.direccion }}</dd>
              <dt class="col-sm-6 text-uppercase text-muted">
                <small>Type:</small>
              </dt>
              <dd class="col-sm-6">{{ selectedFeature.destino_ec }}</dd>
              <dt class="col-sm-6 text-uppercase text-muted">
                <small>Ownership:</small>
              </dt>
              <dd class="col-sm-6">{{ selectedFeature.juridico }}</dd>
            </dl>
            <hr />
          </div>
        </b-collapse>
      </template>
    </app-scroll>
  </div>
</template>
<script>
import Scroll from "@/components/analysis/Scroll"
export default {
  props: ["selectedFeature"],
  components:{
    appScroll: Scroll
  },
  methods: {
    close() {
      this.$emit("close");
    }
  }
};
</script>
<style scoped>
</style>
