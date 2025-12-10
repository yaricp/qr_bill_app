<template>
    <div class="col-md-12">
      <div class="form-group">
        <div v-if="message" class="alert alert-danger" role="alert">
          {{ message }}
        </div>
      </div>
    </div>
</template>
  
<script lang="ts">
  import { defineComponent } from "vue";
  import { ErrorMessage } from "vee-validate";
  import { useStore } from '@/store';

  
  export default defineComponent({
    name: "login_by_tg-page",
    components: {
      // eslint-disable-next-line
      ErrorMessage,
    },
    data() {
      return {
        loading: false,
        message: "",
      };
    },
    computed: {
      loggedIn() {
        const store = useStore();
        console.log("store.state: ", store.state);
        console.log("this.$store.state: ", this.$store.state);
        return store.state.auth.loggedIn;
      },
    },
    async created() {
      console.log("this.loggedIn", this.loggedIn);
      this.loading = true;
      let link = this.$route.params.link
      console.log("link", link);
      try {
        await this.$store.dispatch("auth/verify", link);
        console.log("before go to profile");
        this.$router.push("/profile");
        console.log("this.loggedIn", this.loggedIn);
      } catch(error) {
        this.loading = false;
        this.message = "Problems with authorizate";
      }
    }
});
</script>
