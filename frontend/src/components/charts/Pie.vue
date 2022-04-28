<script>
import { Pie, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
// import randomcolor from "randomcolor";

export default {
  extends: Pie,
  mixins: [reactiveProp],
  mounted() {
    this.renderChart(this.chartData, {
      responsive: true,
      maintainAspectRatio: true
    });
  }
};
</script>
