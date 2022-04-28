<template>
  <div v-if="show" class="info p-2">
    <slot name="header"></slot>
    <app-scroll>
      <template v-slot:content>
        <div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold">Attributes</div>
          <div>
            <span class="heading">Name: </span><span class="value">Area of Interest (AOI) name.</span>
          </div>
          <div>
            <span class="heading">Size: </span><span class="value">area calculated in square kilometers.</span>
          </div>
          <div>
            <span class="heading">Sectors: </span><span class="value">the number of sectors in Area of Interest (AOI).</span>
          </div>
          <div>
            <span class="heading">Buildings: </span><span class="value">number of buildings.</span>
          </div>
          <div>
            <span class="heading">Roof area: </span><span class="value">average (mean) roof area in meters.</span>
          </div>
          <div>
            <span class="heading">Building height: </span><span class="value">average (mean) building height in meters.</span>
          </div>
          <div>
            <span class="heading">Greenspace: </span><span class="value">total area of greenspace designated as cemetery, forest, grass, meadow, park, playing field, recreation ground or scrub in OpenStreetMap.</span>
          </div>
          <div>
            <span class="heading">Roads: </span><span class="value">roads derived from OpenStreetMap; paved or unpaved designation
              visually assessed from drone imagery.
            </span>
          </div>
          <div>
            <span class="heading">Average Tax (where available): </span><span class="value">average property tax.</span>
          </div>
          <div>
            <span class="heading">Average Tax owed (where available): </span><span class="value">average property tax owed.</span>
          </div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold ">
            Analysis
          </div>
          <div>
            <span class="heading">Resettlement: </span>
            <span class="value">
              Demand for resettlement: <strong>yes</strong>, if any hazard=5; total quality=poor or very poor. Otherwise, <strong>no</strong>. This is for illustrative purposes
            </span>
          </div>
          <div>
            <span class="heading">Soft story: </span>
            <span class="value">
              Is this a potential soft story building? <strong>yes</strong> or <strong>no</strong>. For example, the building height is at least 7.5 meters AND has at least one garage AND at least two windows. Other soft story calculations are possible.
            </span>
          </div>
          <div>
            <span class="heading">Public land: </span>
            <span class="value">
              Is the building on public land? <strong>yes</strong> or <strong>no</strong>.
            </span>
          </div>
          <div>
            <span class="heading">Total quality: </span>
            <span class="value">
              Determined by comparing the roof and wall condition derived from drone and street view imagery. If roof and wall condition are not the same designation (good, fair or poor), the lower value of the two is taken.<br/>
              <strong>very good</strong>: if both roof and wall condition are good.<br/>
              <strong>good</strong>: if roof or wall condition is good and the other is under construction, vacant or otherwise unknown.<br/>
              <strong>fair</strong>: if both roof and wall condition are fair; or if one is fair and the other is good, under construction, vacant or otherwise unknown.<br/>
              <strong>poor</strong>: if roof or wall condition is poor and the other is good, fair, under construction, vacant or otherwise unknown.<br/>
              <strong>very poor</strong>: if both roof and wall condition are poor.<br/>
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
            <span class="heading">Area: </span><span class="value">roof area in square meters.</span>
          </div>
          <div>
            <span class="heading">Height: </span><span class="value">building height in meters.</span>
          </div>
          <div>
            <span class="heading">Average tax (where available): </span><span class="value">average property tax.</span>
          </div>
          <div>
            <span class="heading">Average tax owed (where available): </span><span class="value">average property tax owed.</span>
          </div>
          <div class="pt-3 section text-uppercase text-dark font-weight-bold">COVID-19 (where available)</div>
          <div>
            <span class="heading">Covid-19 Vulnerability Index: </span>
            <span class="value">This index locates the bottom-40 and bottom-10 vulnerable households at the block level. Variables correspond to overcrowding, age, illness, disability, and access to water, sewerage, electricity, and internet.</span>
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
