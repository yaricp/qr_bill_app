<template>
    <div class="container" v-if="currentUser">
      <header class="jumbotron">
        <h3>
          Profile with ID:
          <strong>{{ currentUser.id }}</strong>
        </h3>
      </header>
      <p>
        <strong>Id:</strong>
        {{ currentUser.id }}
      </p>
      <p>
        <strong>Login:</strong>
        {{ currentUser.login }}
      </p>
      <p>
        <strong>Email:</strong>
        {{ currentUser.email }}
      </p>
      <p>
        <strong>tg_id:</strong>
        {{ currentUser.tg_id }}
      </p>
      <p>
        <strong>password:</strong>
        {{ currentUser.password_hash }}
      </p>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from "@/store";
import UserService from "@/services/users";
import { IUser } from "@/interfaces/users";
import { checkTokenExpired } from "@/http-common";

export default defineComponent({
  name: 'profile-page',
  data() {
    return {
      currentUser: {} as IUser,
    }
  },
  computed: {
    currentToken() {
      const store = useStore();
      return store.state.auth.token;
    }
  },
  methods: {
    async retrieveUser() {
      console.log("start get User from server");
      try {
        let response = await UserService.getUserProfile(
          this.currentToken
        );
        console.log(response.data);
        this.currentUser = response.data;
      } catch(e) {
        checkTokenExpired(e);
      }
    } 
  },
  async mounted() {
    if (!this.currentToken) {
      this.$router.push('/login');
    }
    console.log("before retrieve User");
    await this.retrieveUser();
  }
});
</script>
