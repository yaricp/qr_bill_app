<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark">
      
      <router-link to="/" class="navbar-brand">Qr Bill Collector</router-link>
      <div class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/qr_scanner" class="nav-link">QRScanner</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/category_analytics" class="nav-link">Category Analytics</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/goods_analytics" class="nav-link">Goods Analytics</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/seller_analytics" class="nav-link">Seller Analytics</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/categories" class="nav-link">Categories</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/goods" class="nav-link">Goods</router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" @click.prevent="logOut">
            <font-awesome-icon icon="sign-out-alt" /> LogOut
          </a>
        </li>
      </div>
    </nav>

    <div class="container mt-3">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    }
  }
});
</script>

<style scoped>
#wrapper {
  max-width: 600px;
  margin: 0 auto;
}
</style>