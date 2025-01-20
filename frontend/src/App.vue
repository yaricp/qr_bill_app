<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid" v-if="loggedIn">
        <a class="navbar-brand" href="#">
          Qr Bill<br>Collector
        </a>
        <div class="navbar-nav">
          <li class="nav-item">
            <router-link to="/qr_scanner" class="nav-link">QRScanner</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/category_goods" class="nav-link">
              Categorize your goods
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'category_analytics', params: { by_months: 1 }}" 
              class="nav-link"
            >
              Analytics by Categories for month
            </router-link>
          </li>
        </div>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <div class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Analytics
            </a>
            <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
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
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Objects
            </a>
            <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
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
            <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
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
        </div>
        </div>
      </div> 
      <div><add-to-home-screen/></div>
      <div>&nbsp;&nbsp;&nbsp;</div>
    </nav>
    <div class="container mt-3">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import AddToHomeScreen from "@/components/utils/addHomeButton.vue";
import { useStore } from '@/store';

export default defineComponent({
  name: "App",
  components: {AddToHomeScreen},
  computed: {
      loggedIn() {
        const store = useStore();
        console.log("store: ", store);
        return store.state.auth.token ? true: false;
      },
    },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    }
  }
});
</script>

<style scoped>
@media screen and (min-width: 992px) {
  .navbar {
    padding: 0;
    line-height: 3rem;
    .dropdown-menu {
      line-height: initial;
    }
  }  
  
  .dropdown {
    .dropdown-menu {
      display: none;
    }
  }
  .dropdown,
  .dropend {
    &:hover {
      & > .dropdown-menu {
        display: block;
      }
    }
  }
  .dropdown {
    &:hover {
      & > .dropdown-menu {
        margin-top: -.5rem;
      }
    }
  }
  .dropend {
    &:hover {
      & > .dropdown-menu {
        position: absolute;
        top: -.5rem;
        left: 100%;
        margin-left: 0;
      }
    }
  }
}
</style>