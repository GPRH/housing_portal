import { mapGetters } from "vuex";

export const InfrastructureMixin = {
  computed: {
    ...mapGetters({
      aoiInfrastructureField: "analysis/getAoiInfrastructureField",
      filters: "filters/getUseFilters",
      aoi: "maps/getSelectedAoi"
    }),
    useFilters() {
      return this.filters.filter(filter => {
        if (filter.id !== "critical") return true;
        else if (
          filter.id === "critical" &&
          this.aoiInfrastructureField.includes(this.aoi.slug)
        ) {
          return true;
        } else {
          return false;
        }
      });
    }
  }
};
