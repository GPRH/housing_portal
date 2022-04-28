<template>
  <b-container id="container" fluid>
    <main class="mx-auto">
      <a id="care" class="pt-2"></a>
        <h1 class="section-title mt-4">What we care about</h1>
        <section class="content d-flex row justfiy-content-start">
          <b-container fluid class="p-4 container-dark">
            <b-row>
              <b-col>
                <b-img class="p-2" src="img/landing/Picture_1.jpg" fluid-grow></b-img>
                <h4 class="title p-2">Saving Lives</h4>
                <p class="p-2">
                  Connect families that live in unsafe homes with government subsidies
                  or credits to make them a safer, stronger and secure asset.
                </p>
              </b-col>
              <b-col>
                <b-img class="p-2" src="img/landing/Picture_2.jpg" fluid-grow></b-img>
                <h4 class="title p-2">Inclusion</h4>
                <p class="p-2">
                  Locate and quantify the most vulnerable households to connect them
                  to the services they need.  Identify the infrastructure gaps that prevent
                  equitable investment and development in cities.
                </p>
              </b-col>
            </b-row>
          </b-container>
          <b-container fluid class="p-4 container-light">
            <b-row>
              <b-col>
                <b-img class="p-2" src="img/landing/Picture_3.jpg" fluid-grow></b-img>
                <h4 class="title p-2">Livability</h4>
                <p class="p-2">
                  Plan public infrastructure investments to make neighborhoods
                  and cities more vibrant and livable, more walkable and
                  more prepared for smart development.
                </p>
              </b-col>
              <b-col>
                <b-img class="p-2" src="img/landing/Picture_4.jpg" fluid-grow></b-img>
                <h4 class="title p-2">Sustainability</h4>
                <p class="p-2">
                  Help confront the climate crisis by identifying saving opportunities
                  in the use of water and energy. Conduct massive valuation and financial
                  simulations to strengthen city finances and fund better.
                </p>
              </b-col>
            </b-row>
          </b-container>
          <b-container fluid class="container-dark">
            <b-row>
              <b-col class="p-4">
                <b-img class="p-2" src="img/landing/Picture_5.jpg" fluid-grow></b-img>
                <h4 class="title p-2">Public Memory</h4>
                <p class="p-2">
                  Record and preserve the intrinsic relationships and heritage between
                  people, businesses, and their assets so that no disaster can erase them.
                </p>
              </b-col>
              <b-col class="covid p-4">
                <b-img class="p-2" src="img/landing/Picture_6.jpg" fluid-grow></b-img>
                <h4 class="p-2 text-light">Community Participation</h4>
                <p class="p-2">
                  Stimulate local economies with low skilled jobs, improve health and educational
                  outcomes and allow families to work and study from home.
                </p>
              </b-col>
            </b-row>
          </b-container>
        </section>
      <section>
        <h1 class="section-title">How we do it</h1>
        <b-row class="content d-flex row justify-content-center">
          <b-col col-md-12>
            <div class="p-3">
              <!-- <p>
                We partner with governments and companies to save lives and strengthen communities and entire
                economies — one house, one neighborhood and one city at at time.
                </p> -->
                <b-row id="images" class="d-flex align-items-center justify-content-center">
                  <b-col md="4" class="d-flex flex-column align-items-center justify-content-center">
                    <b-img src="img/landing/camera.png" fluid></b-img>
                    <div class="caption">360&deg; camera</div>
                  </b-col>
                  <b-col md="4" class="d-flex flex-column align-items-center justify-content-center">
                    <b-img src="img/landing/drone.png" fluid></b-img>
                    <div class="caption">Drone</div>
                  </b-col>
                  <b-col md="4" class="d-flex flex-column align-items-center justify-content-center">
                    <b-img src="img/landing/laptop.png" fluid></b-img>
                    <div class="caption">Machine Learning</div>
                  </b-col>
                </b-row>
                <p class="pt-3">
                  We use machine learning algorithms to extract detailed geospatial data from high resolution images
                  taken from the sky and from the streets. We then combine these predictions with existing health, social and economic datasets
                  to produce house by house maps.  These maps shine light on public and private investment opportunities that will
                  strenghten and protect existing homes.

                </p>
                <p>
                  With more and better geospatial data, we can help governments choose and calibrate the right policy instrument,
                  involve key business partners that could ensure implementation and accelerate ideas into investments before it's too late&#8212;before the next earthquake, hurricane or public health crisis.
                </p>
            </div>
          </b-col>
        </b-row>
      </section>
      <section>
        <div class="covid d-flex p-4 row mt-3 text-wrap" style="font-size: 1.5em;">
          <center>
            <strong>Cost Efficiency and Social Distance:</strong> Our technology allows us to generate an unprecedented amount
            of data at a fraction of the cost in a fraction of the time. Gathering this data from cars and drone imagery allows
            us to maintain safe social distancing practices.
          </center>
        </div>
      </section>
      <footer>
        <h1 class="section-title mt-4">Contact Us</h1>
        <div class="d-flex justify-content-center row">
          <b-container id="contact" fluid class="text-light">
            <b-row class="p-4">
              <b-col class="p-0" md="4">
                <b-img src="img/landing/Logo_GPRH_white.png" fluid width="200"></b-img>
                <p class="mt-3">
                  The <strong class="gprh text-light">Global Program for Resilient Housing</strong> helps communities #BuildBetterBefore
                  a disaster or pandemic strikes to save lives and protect livelihoods after one occurs.
                </p>
                <p class="mt-3">
                  1818 H Street, NW Washington, DC 20433 USA<br/>
                  Tel: +1 (202) 473-1000<br/>
                  Fax: +1 (202) 473-1010<br/>
                  Email: support-gprh@worldbankgroup.org
                </p>
              </b-col>
              <b-col class="pt-1 pl-4" md="2">
                <b-row align-v="start">
                  <b-col>
                    <strong>Categories</strong>
                    <div class="mt-1">
                      <div class="mb-1"><a class="link" href="#" v-scroll-to="'#home'">Home</a></div>
                      <div class="mb-1"><a class="link" href="#" v-scroll-to="'#what'">What we do</a></div>
                      <div class="mb-1"><a class="link" href="#" v-scroll-to="'#care'">What we care about</a></div>
                    </div>
                  </b-col>
                </b-row>
                <b-row align-v="start" class="social">
                  <b-col>
                    <div class="mt-2"><strong>Follow us</strong></div>
                    <div class="mt-2">
                      <!-- <b-img src="img/landing/fb_white.svg" class="pr-2"></b-img> -->
                      <b-link href="https://twitter.com/WBG_Cities" target="_blank"><b-img src="img/landing/tw_white.svg"></b-img></b-link>
                    </div>
                  </b-col>
                </b-row>
              </b-col>
              <b-col class="pt-1 pl-4" md="2">
                <strong>To learn more</strong>
                <p class="mt-2 media">
                  <b-link href="https://soundcloud.com/worldbank/theres-no-place-like-home-resilient-housing" target="_blank"><b-button pill size="sm" class="text-uppercase"><strong>Listen</strong></b-button></b-link>
                </p>
                <p class="media">
                  <b-link href="https://www.worldbank.org/en/topic/disasterriskmanagement/brief/global-program-for-resilient-housing" target="_blank"><b-button pill size="sm" class="text-uppercase"><strong>Read</strong></b-button></b-link>
                </p>
                <p class="media">
                  <b-link href="https://www.youtube.com/c/WorldBank/videos" target="_blank"><b-button pill size="sm" class="text-uppercase"><strong>Watch</strong></b-button></b-link>
                </p>
              </b-col>
              <b-col class="pt-1 pl-4" md="4">
                <contact-form></contact-form>
              </b-col>
            </b-row>
          </b-container>
        </div>
      </footer>
    </main>
  </b-container>
</template>
<script>
import ContactForm from "./ContactForm";
export default {
  components: {
    contactForm: ContactForm
  }
}
</script>
<style scoped>
@media (min-width: 961px){
  main {
    padding: 0 6em 0 6em;
  }
}

@media (max-width: 960px){
  main {
    padding: 0 2em 0 2em;
  }
}
main {
  background-color: white;
  font-family: 'Roboto', sans-serif;
  /* padding: 0 6em 0 6em; */
}
.caption {
  font-family: 'Roboto Regular', sans-serif;
}
.title {
  color: #e11921;
  font-family: 'Roboto Regular', sans-serif;
}
.section-title {
  color: #e11921;
  margin-left: -15px;
  margin-top: 40px;
  margin-bottom: 20px;
  font-family: 'Roboto Regular', sans-serif;
}
.content {
  background-color: #F6EFEE;
  font-size: 1.4em;
  font-family: 'Roboto Light', sans-serif;
  color: #555555;
}
.container-dark {
  background-color: #e8e0de;
  font-family: 'Roboto Light', sans-serif;
}
.container-light {
  background-color: #f3efef;
  font-family: 'Roboto Light', sans-serif;
}
.covid {
  color: white;
  background-color: #e11921;
  font-family: 'Roboto Regular', sans-serif;
}
.person {
  font-family: 'Roboto Light', sans-serif;
}
#contact {
  background-color: #333333;
  color: #bcbcbc;
}
.gprh {
  font-family: 'Roboto Medium', sans-serif;
}
#contact button {
  background: #bcbcbc;
  color: #333333;
  height: 2.5em;
  width: 6.8em;
}
.quote {
  font-size: 1.15em;
}
a.link {
  text-decoration: none;
  color: #f8f9fa !important;
  margin-top: 1em;
}
a.link:hover {
  color: lightgrey !important;
}
.social {
  margin-top: 4rem;
}
.media {
  font-family: "Roboto Medium", sans-serif;
  font-weight: bolder !important;
}
</style>
