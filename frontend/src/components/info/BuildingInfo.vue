<template>
  <div v-if="show" class="info p-2">
    <slot name="header"></slot>
    <app-scroll>
      <template v-slot:content>
        <div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold">Location</div>
          <div>
            <span class="heading">City: </span><span class="value">name of the city where the area of interest is located.</span>
          </div>
          <div>
            <span class="heading">Area of Interest: </span><span class="value">geographic area of focus.</span>
          </div>
          <div>
            <span class="heading">Sector: </span><span class="value">subzone of area of interest, such as a neighborhood.</span>
          </div>
          <div>
            <span class="heading">Address: </span><span class="value">mailing address (when available).</span>
          </div>
          <div>
            <span class="heading">Coordinates: </span><span class="value">geographic coordinates calculated from the centroid of the rooftop.</span>
          </div>
          <div>
            <span class="heading">Geohash: </span><span class="value">alphanumeric string to encode geographic coordinates, which can be used to locate a building of interest by entering it in the search bar.</span>
          </div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold ">
            Attributes
          </div>
          <div>
            <span class="heading">Roof material: </span>
            <span class="value">
              The roof material is derived from drone imagery.<br/>
              <strong>metal</strong>: vast majority of the rooftop is covered in metal (70-90%).<br/>
              <strong>mixed</strong>: there are multiple materials being used to cover the roof/keep the inhabitants dry. Typically this is less than 50% concrete.<br/>
              <strong>concrete</strong>: more than 50% of the rooftop is visibly concrete.<br/>
              <strong>tile</strong>: more than 50% of the rooftop is clay or metal tile.
            </span>
          </div>
          <div>
            <span class="heading">Roof condition: </span>
            <span class="value">
              The condition of the roof is decided based on patching, coloring (rust), and general precarious appearance.<br/>
              <strong>good</strong>: if the roof looks like it is new, well-constructed (has no holes) and very minimal patching or discoloration.<br/>
              <strong>fair</strong>: If the roof is patched, discolored, old looking, but still sturdy. Often these are roofs that look old or drab but you think are still livable/not precarious.<br/>
              <strong>poor</strong>: if the roof is very poor quality, lots of patching, holes, marks of sad fixes, items to hold it down, or bags to stop leaks are common.<br/>
              Otherwise, the building may be under construction, blurred or vacant.
            </span>
          </div>
          <div>
            <span class="heading">Height: </span>
            <span class="value">
              Average (mean) height of the building in meters derived from the rooftop polygon and the digital height information derived from the drone. Calculated using zonal statistics.
            </span>
          </div>
          <div>
            <span class="heading">Ground Slope: </span>
            <span class="value">
              Average (mean) slope of the ground in degrees underneath the roof.
            </span>
          </div>
          <div>
            <span class="heading">Volume: </span>
            <span class="value">
              Estimated volume of building in cubic meters.
            </span>
          </div>
          <div>
            <span class="heading">Roof area: </span>
            <span class="value">
              Estimated roof area in square meters.
            </span>
          </div>
          <div>
            <span class="heading">Average tax (where applicable): </span>
            <span class="value">
              Average property tax per building.
            </span>
          </div>
          <div>
            <span class="heading">Average tax owed (where applicable): </span>
            <span class="value">
              Average property tax owed per building.
            </span>
          </div>
          <!-- <div class="pt-3 section text-uppercase text-dark font-weight-bold ">
            Risks
          </div> -->
          <!-- <div>
            <span class="heading">Designed: </span>
            <span class="value">
              <strong>designed</strong>: this building has been designed at one time.<br>
              <strong>undesigned</strong>: this building was built incrementally.
            </span>
          </div> -->
          <div>
            <span class="heading">Wall material: </span>
            <span class="value">
              <strong>brick or concrete block</strong>; <strong>plaster</strong>; <strong>wood polished</strong>;
              <strong>wood crude plank</strong>; <strong>adobe</strong>;
              <strong>corrugated metal</strong>; <strong>stone with mud/ashlar with lime or concrete</strong>;
              <strong>container/trailer</strong>; <strong>plant material</strong>; <strong>mix/unclear/other</strong>
            </span>
          </div>
          <div>
            <span class="heading">Wall condition: </span>
            <span class="value">
              Derived from street view imagery.<br/>
              <strong>good</strong>: new construction and sturdy.<br/>
              <strong>fair</strong>: sturdy but shows signs of aging.<br/>
              <strong>poor</strong>: dilapidated, temporary, self-built, or not well-maintained.
            </span>
          </div>
          <div>
            <span class="heading">Use: </span>
            <span class="value">
              Derived from street view imagery.<br/>
              <strong>residential</strong>: used solely for residential purposes.<br/>
              <strong>commercial</strong>: used for commercial purposes, such as a store.<br/>
              <strong>critical infrastructure</strong>: used for public purposes, such as education, government, public services, health care, religion, banks or other public infrastructures.<br/>
              <strong>non-residential</strong>: used for commercial or public purposes, such as education, government, public services, health care, religion, banks or other public infrastructures.<br/>
              <strong>mixed</strong>: used for residential and non-residential purposes. A common case is a mini-market on the first floor and residential housing above.<br/>
            </span>
          </div>
          <div>
            <span class="heading">Security: </span>
            <span class="value">
            <strong>secured</strong>, <strong>unsecured</strong>.
            </span>
          </div>
          <div>
            <span class="heading">Construction: </span>
            <span class="value">
            The predominant construction type is organized into the following categories:<br/>
            <strong>Unreinforced masonry</strong>: refers to buildings made from brick, stone or concrete blocks that appear from the outside to be missing concrete columns or beams (or both). Other examples include buildings made from adobe or constructed using timber or wooden frames.<br/>
            <strong>Reinforced masonry</strong>: refers to buildings with confined masonry or concrete frames, which may be called reinforced masonry in some countries. Reinforcement components such as rebar inside of blocks are not always possible to determine from street view analysis but at times, particularly when buildings are ‘incomplete’ rebar is visible.<br/>
            <strong>Unknown</strong>: unknown.
            </span>
          </div>
          <div>
            <span class="heading">Vintage: </span>
            <span class="value">
            1) <strong>Pre 1940</strong>, 2) <strong>1941-1974</strong>, 3) <strong>1975-1999</strong>, 4) <strong>2000-now</strong>
            </span>
          </div>
          <div>
            <span class="heading">Complete: </span>
            <span class="value">construction status of the building, <strong>complete</strong> or <strong>incomplete</strong></span>
          </div>
          <div>
            <span class="heading">Public land: </span>
            <span class="value">indicates if a building is on public land, <strong>yes</strong> or <strong>no</strong></span>
          </div>
          <!-- <div>
            <span class="heading">Disaster: </span>
            <span class="value">
            Is there disaster mitigation measure that the house has built? <strong>1</strong> = yes, <strong>0</strong> = no
            </span>
          </div> -->
          <div class="mt-3">
            <span class="heading">Drone confidence levels</span>
            <p>
              The drone confidence level defines how certain the model is to determine the roof material and condition.
              For each roof, the machine learning model calculates an array of values equal to the number of potential classifications
              and assigns the probability of each a value between 0-1, with 1 equaling 100% probability.
            </p>
            <p>
              The confidence level measures the difference of the material (or condition) with the highest probability minus the rest of the values of the array.
            </p>
            <strong>high</strong>: if the value is &gt;0.75, the difference among the material (or condition) with the highest probability and the rest is large, the confidence is high.<br/>
            <strong>medium</strong>: if the value is &gt;0.25 and &lt;0.75, there is a material (or condition) that has a higher probability than the rest, but the difference is not clear, so the confidence is medium.<br/>
            <strong>low</strong>: if the difference is &lt;0.25, the model cannot clearly differentiate between at least two materials (or conditions), so the confidence is low.<br/>
          </div>
          <div class="mt-2">
            <span class="heading">Street view confidence levels</span>
            <p>
              The identification of a building characteristic depends on how clear it is in the image and how many training samples of the characteristic were provided in the machine learning model.
            </p>
            <p>
              Each prediction receives a prediction score between 0-1, with 1 being the most confident.
            </p>
            <p>
              With multiple street view images of the same building, a building characteristic is determined by the highest prediction score among all images. Prediction scores are grouped from highest to lowest in three equally-sized categories to establish <strong>high</strong>, <strong>medium</strong>, and <strong>low</strong> confidence levels for each building characteristic.
            </p>
            <p>
              If prediction scores for a building characteristic are all greater than 0.95, then all predictions for that building characteristic are assigned high confidence.
            </p>
          </div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold ">
            Analysis
          </div>
          <div>
            <span class="heading">Resettlement: </span>
            <span class="value">
            Demand for resettlement: <strong>yes</strong>, if any hazard=5; total quality=poor or very poor. Otherwise, <strong>no</strong>. This is for illustrative purposes.
            </span>
          </div>
          <div>
            <span class="heading">Soft story: </span>
            <span class="value">
              Is this a potential soft story building? <strong>yes</strong> or <strong>no</strong>. For example, the building height is at least
              7.5 meters AND has at least one garage AND at least two windows. Other soft story calculations are possible.
            </span>
          </div>
          <div>
            <span class="heading">Structural improvement: </span>
            <span class="value">
            Demand for structural improvement: <strong>yes</strong>, if earthquake hazzard is 3 or lower AND flood, landslide or wind hazzard is between
            0 and 4 AND construction type=unreinforced masonry or reinforced masonry AND soft story=yes AND total quality=good or fair. Otherwise, <strong>no</strong>.
            </span>
          </div>
          <div>
            <span class="heading">Quality improvement: </span>
            <span class="value">
            Demand for quality improvement: <strong>yes</strong>, if hazards are below 5 AND construction type=reinforced masonry AND possible soft story=yes
            AND total quality=fair, poor or very poor. Otherwise, <strong>no</strong>.
            </span>
          </div>
          <div>
            <span class="heading">Expansion: </span>
            <span class="value">
            Opportunity for expansion: <strong>yes</strong>, if building height is less than 3 meters AND within 200 meters of greenspace AND within 5 meters of paved road. Otherwise, <strong>no</strong>.
            </span>
          </div>
          <div>
            <span class="heading">Payment capacity: </span>
            <span class="value">
            Capacity of payment from households: maximum household annual income=(estimated value/5). Estimated value can be modeled from field surveys. This is for illustrative purposes.
            </span>
          </div>
          <div>
            <span class="heading">Home insurance: </span>
            <span class="value">
            Demand for home insurance premiums: <strong>yes</strong>, if total quality is good or very good; all other demands=no; and general value=medium or high. Otherwise, <strong>no</strong>.
            General value can be calcuated from the total quality and building volume, determined per AOI. This is for illustrative purposes.
            </span>
          </div>
          <div>
            <span class="heading">Home microfinance: </span>
            <span class="value">
            Demand for home improvement microloans: <strong>yes</strong>, if ONLY demand for quality improvement=yes AND structural improvements=yes;
            and capacity of payment &gt;$10,000. This is for illustrative purposes.
            </span>
          </div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold">COVID-19 (where available)</div>
          <div>
            <span class="heading">Covid-19 Vulnerability Index: </span>
            <span class="value">This index locates the bottom-40 and bottom-10 vulnerable households at the block level. Variables correspond to overcrowding, age, illness, disability, and access to water, sewerage, electricity, and internet.
              Values range from 1-3 with 1 being the most vulnerable.
            </span>
          </div>
        </div>
      </template>
    </app-scroll>
  </div>
</template>
<script>
import Scroll from "@/components/analysis/Scroll";
export default {
  props: ["show"],
  components: {
    appScroll: Scroll
  }
}
</script>
<style scoped>
.info {
  width: 30vw;
  height: 65vh;
  background-color: white;
  border-radius: 0px;
  border: none;
  overflow: hidden;
  pointer-events: all;
}
.section {
  font-size: 1em;
}
.heading {
  color: #C63D39;
  font-size: 1em;
  font-weight: bold;
}
</style>
