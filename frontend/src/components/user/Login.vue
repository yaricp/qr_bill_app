<template>
    <div class="col-md-12">
      <div class="card card-container">
        <Form @submit="handleLogin" :validation-schema="schema">
          <div class="form-group">
            <label for="login">Login</label>
            <Field name="login" type="text" class="form-control" />
            <ErrorMessage name="login" class="error-feedback" />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <Field name="password" type="password" class="form-control" />
            <ErrorMessage name="password" class="error-feedback" />
          </div>
  
          <div class="form-group">
            <button class="btn btn-primary btn-block" :disabled="loading">
              <span
                v-show="loading"
                class="spinner-border spinner-border-sm"
              ></span>
              <span>Login</span>
            </button>
          </div>
  
          <div class="form-group">
            <div v-if="message" class="alert alert-danger" role="alert">
              {{ message }}
            </div>
          </div>
        </Form>
      </div>
    </div>
</template>
  
<script lang="ts">
  import { defineComponent } from "vue";
  import { Form, Field, ErrorMessage } from "vee-validate";
  import * as yup from "yup";
  import { useStore } from '@/store';
  import { IUserLogin } from "@/interfaces/users";
  
  export default defineComponent({
    name: "login-page",
    components: {
      // eslint-disable-next-line
      Form,
      Field,
      ErrorMessage,
    },
    data() {
      const schema = yup.object().shape({
        login: yup
        .string()
        .required("Login is required!"),
        password: yup
        .string()
        .required("Password is required!"),
      });
      return {
        loading: false,
        message: "",
        schema,
      };
    },
    computed: {
      loggedIn() {
        const store = useStore();
        console.log("store: ", store);
        return store.state.auth.loggedIn;
      },
    },
    created() {
      if (this.loggedIn) {
        this.$router.push("/qr_scanner");
      }
    },
    methods: {
      async handleLogin(user: IUserLogin) {
        this.loading = true;
        try {
          await this.$store.dispatch("auth/login", user);
          console.log("before go to profile");
          this.$router.push("/qr_scanner");
        } catch(error) {
          console.log("Error: ", error);
          this.loading = false;
          this.message = "Problems with authorizate";
        }
      },
    },
});
</script>
