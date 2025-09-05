<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg bg-light">
      <a class="navbar-brand" href="/main">
        qr_bill_app<br>
      </a>
      <div class="navbar-nav" v-if="!loggedIn">
        <li class="nav-item">
          <router-link to="/about/" class="nav-link">
            {{ $t("menu.about") }}
          </router-link>
        </li>
      </div>
      <div class="container-fluid" v-if="loggedIn">
        <div class="navbar-nav">
          <li class="nav-item">
            <router-link to="/qr_scanner" class="nav-link">
              {{ $t("menu.scanner") }}
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/category_products" class="nav-link">
              {{ $t("menu.cat_goods") }}
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              :to="{ name: 'category_analytics', params: { by_months: 1 }}" 
              class="nav-link"
            >
            {{ $t("menu.cat_month_analytic") }}
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
                {{ $t("menu.analytics.head") }}
              </a>
              <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
                <li>
                  <router-link to="/category_analytics" class="dropdown-item">
                    {{ $t("menu.analytics.categories") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/goods_analytics" class="dropdown-item">
                    {{ $t("menu.analytics.goods") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/seller_analytics" class="dropdown-item">
                    {{ $t("menu.analytics.sellers") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/product_prices" class="dropdown-item">
                    {{ $t("menu.analytics.product_prices") }}
                  </router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                {{ $t("menu.lists.head") }}
              </a>
              <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
                <li>
                  <router-link to="/categories" class="dropdown-item">
                    {{ $t("menu.lists.categories") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/bills" class="dropdown-item">
                    {{ $t("menu.lists.bills") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/goods" class="dropdown-item">
                    {{ $t("menu.lists.goods") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/sellers" class="dropdown-item">
                    {{ $t("menu.lists.sellers") }}
                  </router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                {{ $t("menu.user.head") }}
              </a>
              <ul class="dropdown-menu dropdown-menu-light" aria-labelledby="dropdownMenuButton1">
                <li>
                  <router-link to="/profile" class="dropdown-item">
                    {{ $t("menu.user.profile") }}
                  </router-link>
                </li>
                <li>
                  <router-link to="/logout" class="dropdown-item">
                    {{ $t("menu.user.logout") }}
                  </router-link>
                </li>
                <li v-if="isAdmin">
                  <router-link to="/users" class="dropdown-item">
                    {{ $t("menu.user.users") }}
                  </router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link to="/about/" class="nav-link">
                {{ $t("menu.about") }}
              </router-link>
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
        return store.state.auth.token ? true: false;
      },
      isAdmin() {
        const store = useStore();
        return store.state.auth.isAdmin ? true: false;
      },
      lang() {
        const store = useStore();
        return store.state.auth.lang;
      }
    },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    }
  },
  mounted() {
    this.$i18n.locale = this.lang;
  },
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