<template>
<div>
  <b-form @submit.prevent="submit" class="mb-2">
      <b-form-group
        id="contact-email"
        label-for="email"
      >
        <b-form-input
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="Email"
        ></b-form-input>
      </b-form-group>
      <b-form-group id="contact-name" label-for="name">
        <b-form-input
          id="name"
          v-model="name"
          required
          placeholder="Name"
        ></b-form-input>
      </b-form-group>
      <b-form-group id="contact-message" label-for="message">
        <b-form-textarea
          id="message"
          v-model="message"
          required
          placeholder="Message"
        ></b-form-textarea>
      </b-form-group>
      <b-button disabled type="submit" class="float-right" v-if="dismissCountDown===0">Send</b-button>
  </b-form>
  <b-alert
    fade
    variant="success"
    :show="dismissCountDown"
    @dismissed="dismissForm"
    @dismiss-count-down="countDownChanged">
      Thank you! Your message has been sent.
  </b-alert>
  <b-alert fade dismissible variant="danger" :show="error" @dismissed="error===false">
    There was an error sending your request. Please try again later or
    contact us using the contact details on this page.
  </b-alert>
</div>
</template>
<script>
const CONTACT_FORM_AUTH_TOKEN = process.env.VUE_APP_CONTACT_FORM_AUTH_TOKEN;
import axios from "axios";
let authAxios = axios.create({
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  withCredentials: true
});
export default {
  data(){
    return {
      auth_token: CONTACT_FORM_AUTH_TOKEN,
      email: null,
      name: null,
      message: null,
      error: false,
      dismissSecs: 3,
      dismissCountDown: 0
    }
  },
  methods: {
    async submit() {
      try {
        let response = await authAxios.post("/api/geodata/contact/", {
          auth_token: this.auth_token,
          email: this.email,
          name: this.name,
          message: this.message
        });
        if(response.status === 200) {
          this.dismissCountDown = this.dismissSecs;
        }
      } catch(error){
        this.error = true;
      }
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    dismissForm(){
      this.dismissCountDown = 0;
      this.email = '',
      this.name = '',
      this.message = ''
    }
  }
}
</script>
<style scoped>
button {
  color: whitesmoke !important;
  background: black !important;
  border-color: black !important;
  height: 2.5em;
  width: 6.8em;
  border-radius: 0px;
}
.form-control {
  background-color: #E4E4E4;
  border-radius: 0px;
}
.form-control:focus {
  border-color: #333333;
  -webkit-box-shadow: 0 0 0 0.2rem rgba(188,188,188,0.25);
  box-shadow: 0 0 0 0.2rem rgba(188, 188, 188, 0.25);
}

</style>
