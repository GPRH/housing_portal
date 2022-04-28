<template>
  <v-select id="aoi-select"
    class="aoi-selector"
    v-model="selectedAoi"
    :options="options"
    @input="aoiSelected()"
    :clearable="false"
    :searchable="false"
    label="city"
    :placeholder="'Select Area of Interest'">
    <template #open-indicator>
      <span class="text-muted font-weight-bold"><b-icon-caret-down-fill></b-icon-caret-down-fill></span>
    </template>
    <template #selected-option="option">
      <div style="display: flex; align-items: baseline;">
      <span class="text-uppercase font-weight-bolder text-muted">{{ option.name }}</span>
      </div>
    </template>
    <template v-slot:option="option">
      <span style="margin: 0">{{ option.name }}  <em>({{ option.city }})</em></span>
    </template>
  </v-select>
</template>
<script>
export default {
  data(){
    return {
      aois: [],
    }
  },
  computed: {
      selectedAoi: {
        get () {
          return this.$store.state.maps.selectedAOI;
        },
        set (value) {
          this.$store.commit('maps/setSelectedAoi', value);
        }
      },
      country() {
        return process.env.VUE_APP_PORTAL_COUNTRY;
      },
      options(){
        return _.sortBy(this.aois, ['city', 'name']);
      },
      aoi() {
        return this.$store.getters["maps/getSelectedAoi"];
      },
    },
    methods: {
      async loadAois(){
        await this.$store.dispatch("maps/loadAOIS");
        this.aois = this.$store.getters["maps/getAois"];
      },
      aoiSelected(){
        this.$emit('aoi-selected');
      }
  },
  created(){
    this.loadAois();
  },
}
</script>
<style>
#aoi-select {
  min-width: 210px;
  margin-left: -8px;
}
#vs1__combobox {
  border: none;
}
#aoi-select li.vs__dropdown-option.vs__dropdown-option--highlight {
  background:#6c757d !important
}
#aoi-select input::placeholder {
  color: rgba(0, 0, 0, 0.5);
  font-weight: bolder;
}
</style>
