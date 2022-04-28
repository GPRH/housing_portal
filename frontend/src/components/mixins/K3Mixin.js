import { mapGetters } from "vuex";

export const K3Mixin = {
  computed: {
    ...mapGetters({
      covidFields: "analysis/getAoiCovidFields",
      aoi: "maps/getSelectedAoi"
    }),
    displayCovid() {
      //  whether covid k3 index is available and should be
      //  displayed for this AOI
      return this.covidFields.includes(this.aoi.slug);
    }
  }
};
