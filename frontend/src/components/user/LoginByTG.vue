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
  // import { useRoute } from 'vue-router'

  
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
    created() {
      console.log("this.loggedIn", this.loggedIn);
      if (this.loggedIn) {
        this.$router.push("/goods");
      } else {
        this.loading = true;
        let link = this.$route.params.link
        console.log("link", link);
        this.$store.dispatch("auth/login_by_tg", link).then(
          () => {
            console.log("before go to goods");
            this.$router.push("/goods");
          },
          (error) => {
            this.loading = false;
            this.message =
              (error.response &&
                error.response.data &&
                error.response.data.message) ||
              error.message ||
              error.toString();
          }
        );
      }
    }
});
</script>
