<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark">
      <router-link to="/" class="navbar-brand">Qr Bill Collector</router-link>
      <div class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link to="/qr_scanner" class="nav-link">QRScanner</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/goods_analytics" class="nav-link">Goods Analytics</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/seller_analytics" class="nav-link">Seller Analytics</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/goods" class="nav-link">Goods</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/add" class="nav-link">Add</router-link>
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
});
</script>