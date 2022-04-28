<template>
  <div class="login d-flex align-items-center">
    <div class="container">
      <b-row class="justify-content-center h-100">
        <b-col md="8">
          <b-card-group>
            <b-card no-body class="p-4">
              <b-card-body>
                <b-form>
                  <h1>Login</h1>
                  <p class="text-muted">Login to the housing portal</p>
                  <div
                    class="alert alert-danger"
                    v-show="invalidLogin"
                  >Invalid username or password.</div>
                  <b-input-group class="mb-3">
                    <b-form-input
                      name="email"
                      type="text"
                      class="form-control"
                      placeholder="Email"
                      autocomplete="email"
                      v-validate="'required|email'"
                      v-model="email"
                      :state="validateState('email')"
                      @input="invalidLogin = false"
                    />
                    <b-form-invalid-feedback id="email">
                      <ul>
                        <li v-for="error in errors.collect('email')">{{ error }}</li>
                      </ul>
                    </b-form-invalid-feedback>
                  </b-input-group>
                  <b-input-group class="mb-4">
                    <b-form-input
                      name="password"
                      type="password"
                      class="form-control"
                      placeholder="Password"
                      autocomplete="current-password"
                      v-model="password"
                      v-validate="'required'"
                      :state="validateState('password')"
                      @input="invalidLogin = false"
                    />
                    <b-form-invalid-feedback id="password">
                      <ul>
                        <li v-for="error in errors.collect('password')">{{ error }}</li>
                      </ul>
                    </b-form-invalid-feedback>
                  </b-input-group>
                  <b-row>
                    <b-col cols="6">
                      <b-button
                        variant="primary"
                        class=""
                        @click="login"
                        :disabled="errors.any()"
                      >
                      <b-icon icon="power" aria-hidden="true"></b-icon> Login
                      </b-button>
                    </b-col>
                    <b-col cols="6" class="text-right">
                      <b-button
                        variant="link"
                        to="/account/password-reset"
                        class="px-0"
                      >Forgot password?</b-button>
                    </b-col>
                  </b-row>
                </b-form>
              </b-card-body>
            </b-card>
          </b-card-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import { ValidationMixin } from "../../components/mixins/ValidationMixin.js";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      password: "",
      invalidLogin: false
    };
  },
  mixins: [ValidationMixin],
  methods: {
    async login() {
      this.$validator.validateAll().then(async () => {
        if (!this.errors.any()) {
          try {
            await this.$store.dispatch("postLogin", {
              email: this.email,
              password: this.password
            });
            this.$router.replace(this.$route.query.redirect || "/portal");
          } catch (error) {
            if (error.response) {
              this.invalidLogin = true;
            }
          }
        }
      });
    }
  }
};
</script>
<style scoped>
.login {
  height: 100vh;
}
</style>
