<template>
    <div class="col-md-12">
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
            <center><h2>{{ $t("register.header" )}}</h2></center>
          </div>
        </div>
        <Form @submit="handleRegister" :validation-schema="schema">
          <div v-if="!successful">
            <div class="form-group">
              <label for="login">{{ $t("register.login" )}}</label>
              <Field name="login" type="login" class="form-control" />
              <ErrorMessage name="login" class="error-feedback" />
            </div>
            <div class="form-group">
              <label for="password">{{ $t("register.password" )}}</label>
              <Field name="password" type="password" class="form-control" />
              <ErrorMessage name="password" class="error-feedback" />
            </div>
            <div class="form-group">
              <label for="password2">{{ $t("register.password2" )}}</label>
              <Field name="password2" type="password" class="form-control" />
              <ErrorMessage name="password2" class="error-feedback" />
            </div>
            <div class="form-group">
              <div class="row">
                <div class="col">
                  <input 
                    class="form-check-input" 
                    type="checkbox"
                    v-model="agreement_accepted" 
                    id="flexCheckDefault"
                  >
                </div>
                <div class="col">
                  {{ $t("agreement.register_text") }}
                  <router-link to="/agreement/">
                    {{ $t("agreement.register_link") }}
                  </router-link>
                </div>
              </div>
            </div>
            <div class="form-group" v-if="agreement_accepted">
              <button class="btn btn-primary btn-block" :disabled="loading">
                <span
                  v-show="loading"
                  class="spinner-border spinner-border-sm"
                ></span>
                {{ $t("register.reg_btn" )}}
              </button>
            </div>
            <div class="form-group">
              {{ $t("register.login_text") }}
              <router-link to="/login/">
                {{ $t("register.login_link") }}
              </router-link>
            </div>
          </div>
        </Form>
        <div
          v-if="message"
          class="alert"
          :class="successful ? 'alert-success' : 'alert-danger'"
        >
          {{ message }}
        </div>
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
  name: "register-page",
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
        .required("Password is required!")
        .min(6, "Must be at least 6 characters!")
        .max(40, "Must be maximum 40 characters!"),
      password2: yup
        .string()
        .required("Repeat Password is required!")
        .min(6, "Must be at least 6 characters!")
        .max(40, "Must be maximum 40 characters!"),
    });
    return {
      lang: "en" as string,
      successful: false as boolean,
      loading: false as boolean,
      message: "" as string,
      agreement_accepted: false as boolean,
      schema,
    };
  },
  methods: {
    async handleRegister(user: IUserLogin) {
      this.message = "";
      this.successful = false;
      this.loading = true;
      try {
        let response = await this.$store.dispatch("auth/register", user);
        console.log("response:", response);
        console.log("response.data:", response.data);
        this.message = String(response.data.message);
        if (response.data.message == "User registered successfull") {
          this.successful = true;
          this.loading = false;
          await this.$nextTick();
          await this.delay(2000);
          this.$router.push("login");
        } else {
          console.log("response.data.message:", response.data.message);
          this.successful = false;
          this.loading = false
        }
        
      } catch (err) {
        this.message = String(err);
        this.successful = false;
        this.loading = false
      }
    },
    async delay(ms:number) {
      return new Promise(res => setTimeout(res, ms));
    }
  },
});
</script>