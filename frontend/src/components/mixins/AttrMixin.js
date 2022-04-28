import { mapGetters } from "vuex";

export const AttrMixin = {
  computed: {
    ...mapGetters({
      includeAttrs: "analysis/getAoiIncludeAttrs",
      aoi: "maps/getSelectedAoi"
    })
  },
  methods: {
    displayAttr(attr) {
      //  whether an attribute should be displayed for this AOI
      if (this.includeAttrs.hasOwnProperty(attr)) {
        const config = this.includeAttrs[attr];
        if (config) {
          return config.includes(this.aoi.slug);
        } else {
          return false;
        }
      } else {
        return true;
      }
    }
  }
};
