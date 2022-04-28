import { mapGetters } from "vuex";

export const TaxMixin = {
  computed: {
    ...mapGetters({
      taxFields: "analysis/getAoiTaxFields",
      aoi: "maps/getSelectedAoi"
    }),
    displayTaxes() {
      //  whether tax info is available and should be
      //  displayed for this AOI
      return this.taxFields.includes(this.aoi.name.toLowerCase());
    },
    averageTaxes() {
      // calculate average taxes at AOI and Sector level.
      if (this.displayTaxes) {
        return (
          this.result.buildings.taxes.total_taxes /
          this.result.buildings.taxes.total_tax_records
        );
      } else {
        return 0;
      }
    },
    averageTaxesOwed() {
      // calculate average taxes at AOI and Sector level.
      if (this.displayTaxes) {
        return (
          this.result.buildings.taxes.total_taxes_owed /
          this.result.buildings.taxes.total_tax_records
        );
      } else {
        return 0;
      }
    }
  }
};
