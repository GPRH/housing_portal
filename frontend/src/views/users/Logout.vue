<template>
  <div class="logout d-flex align-items-center">
    <div class="container">
      <b-row class="justify-content-center">
        <b-col md="8">
          <b-card-group>
            <b-card no-body class="p-4">
              <b-card-body>
                <h1>Logout</h1>
                <p class="text-muted">Are you sure you want to logout?</p>
                <b-row>
                  <b-col cols="6">
                    <b-button
                      variant="primary"
                      class=""
                      @click="logout"
                    >
                      <b-icon icon="power" aria-hidden="true"></b-icon> Logout
                    </b-button>
                    <router-link :to="{name: 'MapViewer'}">
                      <b-button id="cancelLogout" variant="danger" class="ml-3">Cancel</b-button>
                    </router-link>
                  </b-col>
                </b-row>
              </b-card-body>
            </b-card>
          </b-card-group>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
  name: "Logout",
  methods: {
    logout() {
      this.$store.dispatch("postLogout");
      this.$root.$emit('logout');
      this.$router.replace("/");
    }
  }
};
</script>

<style lang="scss" scoped>
.logout {
  height: 100vh;
}
</style>
