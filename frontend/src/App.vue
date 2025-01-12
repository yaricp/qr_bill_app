<template>
  <div id="app">
    <nav class="navbar navbar-expand navbar-dark bg-dark">
      
      <router-link to="/" class="navbar-brand">Qr Bill<br>Collector</router-link>
      <div class="navbar-nav mr-auto">
        
        <li class="nav-item">
          <router-link to="/qr_scanner" class="nav-link">QRScanner</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Analytics
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1">
            <li>
              <router-link to="/category_analytics" class="dropdown-item">
                Category Analytics
              </router-link>
            </li>
            <li>
              <router-link to="/goods_analytics" class="dropdown-item">
                Goods Analytics
              </router-link>
            </li>
            <li>
              <router-link to="/seller_analytics" class="dropdown-item">
                Seller Analytics
              </router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item">
          <router-link to="/category_goods" class="nav-link">Categorize<br>your goods</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Objects
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1">
            <li>
              <router-link to="/categories" class="dropdown-item">
                Categories
              </router-link>
            </li>
            <li>
              <router-link to="/bills" class="dropdown-item">
                Bills
              </router-link>
            </li>
            <li>
              <router-link to="/goods" class="dropdown-item">
                Goods
              </router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            User
          </a>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1">
            <li>
              <router-link to="/profile" class="dropdown-item">
                Profile
              </router-link>
            </li>
            <li>
              <router-link to="/logout" class="dropdown-item">
                Logout
              </router-link>
            </li>
          </ul>
        </li>
        <li class="nav-item">
          <add-to-home-screen/>
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
import AddToHomeScreen from "@/components/utils/addHomeButton.vue";

export default defineComponent({
  name: "App",
  components: {AddToHomeScreen},
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