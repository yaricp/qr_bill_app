<template>
    <div class="container">
      <div class="card card-container">
        <div class="row">
          <div class="col">
            <strong>{{ $t('change_lang')}}</strong>
          </div>
          <div class="col">
            <div class="locale-changer">
              <select 
                v-model="$i18n.locale"
              >
                <option 
                  v-for="locale in $i18n.availableLocales" 
                  :key="`locale-${locale}`" 
                  :value="locale">{{ $t("lang." + locale) }}
                </option>
              </select>
            </div>
        </div>
      </div>
        <div class="row">
          <div class="col">
            <center><h2>{{ $t("login.header" )}}</h2></center>
          </div>
        </div>
        <Form @submit="handleLogin" :validation-schema="schema">
          <div class="form-group">
            <label for="login">{{ $t("login.login" )}}</label>
            <Field name="login" type="text" class="form-control" />
            <ErrorMessage name="login" class="error-feedback" />
          </div>
          <div class="form-group">
            <label for="password">{{ $t("login.password" )}}</label>
            <Field name="password" type="password" class="form-control" />
            <ErrorMessage name="password" class="error-feedback" />
          </div>
  
          <div class="form-group">
            <button class="btn btn-primary btn-block" :disabled="loading">
              <span
                v-show="loading"
                class="spinner-border spinner-border-sm"
              ></span>
              <span>{{ $t("login.login_btn" )}}</span>
            </button>
          </div>
  
          <div class="form-group">
            <div v-if="message" class="alert alert-danger" role="alert">
              {{ message }}
            </div>
          </div>
        </Form>
      </div>
      <div class="row"><hr></div>
      <div class="card card-container">
        <div class="row">
          <div class="col">
            {{ $t("login.you_can_use" )}}&nbsp;
            <a href="https://t.me/qr_bill_app_bot">
              https://t.me/qr_bill_app_bot
            </a>
            &nbsp;{{ $t("login.to_login_link" )}}
          </div>
          <div class="col">
            {{ $t("login.go_to_registration" )}}
            <router-link to="/register/">
              {{ $t("login.registration") }}
            </router-link>
          </div>
        </div>
         
      </div>
      <div class="row"><hr></div>
      <div class="card card-container">
        <small style="color: red;">{{ $t("attantion") }}</small>
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
        lang: "" as string,
        loading: false as boolean,
        message: "" as string,
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
        this.$router.push("/main");
      }
    },
    methods: {
      async handleLogin(user: IUserLogin) {
        this.loading = true;
        try {
          let response = await this.$store.dispatch("auth/login", user);
          console.log("response: ", response);
          if(this.loggedIn){
            this.$router.push("/main");
          } else {
            if (response == 401){
              this.message = "Wrong login or password!";
            } else {
              this.message = "Problems with authorizate";
            }
            this.loading = false;
          }
        } catch(error) {
          console.log("Error: ", error);
          this.loading = false;
          this.message = "Problems with authorizate";
        }
      }
    },
});
</script>
