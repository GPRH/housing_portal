import { mapGetters } from "vuex";

export const SurveyMixin = {
  computed: {
    ...mapGetters({
      surveyFields: "analysis/getAoiSurveyFields",
      aoi: "maps/getSelectedAoi"
    }),
    displaySurvey() {
      //  whether survey data is available and should be
      //  displayed for this AOI
      return this.surveyFields.includes(this.aoi.slug);
    }
  }
};
