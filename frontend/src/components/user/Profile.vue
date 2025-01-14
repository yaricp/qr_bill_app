<template>
    <div class="container" v-if="currentUser">
      <div class="row">
        <header class="jumbotron">
          <h3>
            Profile with ID:
            <strong>{{ currentUser.id }}</strong>
          </h3>
        </header>
      </div>
      <div class="row">
        <div class="col"><strong>Id:</strong></div>
        <div class="col">{{ currentUser.id }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>Login:</strong></div>
        <div class="col">
          <span 
            v-if="login_password_created && !login_password_open_for_edit"
          >{{ currentUser.login }}</span>
          <span v-if="login_password_open_for_edit">
            <input type="text" v-model="currentUser.login">
          </span>
          &nbsp;&nbsp;
          <span>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="!login_password_open_for_edit"
              @click="login_password_open_for_edit =!login_password_open_for_edit"
            >
              Change
            </button>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="login_password_created && login_password_open_for_edit"
              @click="login_password_open_for_edit =!login_password_open_for_edit"
            >
              Close
            </button>
          </span> 
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ login_mess }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>password:</strong></div>
        <div class="col">
          <span 
            v-if="login_password_created && !login_password_open_for_edit"
          >{{ password1 }}</span>
          <span v-if="login_password_open_for_edit">
            <input type="password" v-model="password1">
          </span>
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ password1_mess }}</div>
      </div>
      <div class="row">
        <div class="col"><strong>repeat password:</strong></div>
        <div class="col">
          <span 
            v-if="login_password_created && !login_password_open_for_edit"
          >{{ password2 }}</span>
          <span v-if="login_password_open_for_edit">
            <input type="password" v-model="password2">
          </span>
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ password2_mess }}</div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button 
            class="btn btn-outline-secondary"
            type="button"
            v-if="login_password_created && login_password_open_for_edit"
            @click="saveUserLoginPassword"
          >
            Update Login and/or password
          </button>
          <button 
            class="btn btn-outline-secondary"
            type="button"
            v-if="!login_password_created"
            @click="saveUserLoginPassword"
          >
            Create Login and password
          </button>
        </div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col"><strong>Email:</strong></div>
        <div class="col">
          <span v-if="email_linked && !email_open_for_edit"> {{ currentUser.email }} </span>
          <span v-if="email_open_for_edit">
            <input type="text" v-model="currentUser.email">
          </span>
          <span>
            <button
              v-if="!email_open_for_edit"
              @click="email_open_for_edit =!email_open_for_edit"
            >
              Change
            </button>
            <button
              v-if="email_linked && email_open_for_edit"
              @click="email_open_for_edit =!email_open_for_edit"
            >
              Close
            </button>
          </span> 
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ email_mess }}</div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="!email_linked">Link Email</button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="email_linked && email_open_for_edit">Relink Email</button>
        </div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col"><strong>tg_id:</strong></div>
        <div class="col">
          <span v-if="tg_linked && !tg_open_for_edit"> {{ currentUser.tg_id }} </span>
          <span v-if="tg_open_for_edit">
            <input type="text" v-model="currentUser.tg_id">
          </span>
          &nbsp;&nbsp;
          <span>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="!tg_open_for_edit" 
              @click="tg_open_for_edit =!tg_open_for_edit"
            >
              Change
            </button>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="tg_linked && tg_open_for_edit" 
              @click="tg_open_for_edit =!tg_open_for_edit"
            >
              Close
            </button>
          </span> 
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ tg_mess }}</div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button 
            class="btn btn-outline-secondary"
            type="button"
            v-if="!tg_linked">Link Telegram</button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="tg_linked && tg_open_for_edit">Relink Telegram</button>
        </div>
      </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import UserService from "@/services/users";
import { IUser, IUserLogin } from "@/interfaces/users";
import { useStore } from '@/store';
import { checkTokenExpired } from "@/http-common";

export default defineComponent({
  name: 'profile-page',
  data() {
    return {
      currentUser: {} as IUser,
      login_mess: "" as string,
      password1: "" as string,
      password1_mess: "" as string,
      password2: "" as string,
      password2_mess: "" as string,
      login_password_created: false as boolean,
      login_password_open_for_edit: false as boolean,
      email_linked: false as boolean,
      email_mess: "" as string,
      email_open_for_edit: false as boolean,
      tg_linked: false as boolean,
      tg_mess: "" as string,
      tg_open_for_edit: false as boolean,
    }
  },
  computed: {
    authToken() {
      const store = useStore();
      console.log("store: ", store);
      return store.state.auth.token;
    },
  },
  methods: {
    async retrieveUser() {
      console.log("start get User from server");
      try {
        let response = await UserService.getUserProfile(
          this.authToken
        );
        console.log("retrieveUser: ", response.data);
        this.currentUser = response.data;
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async saveUserLoginPassword() {
      console.log("saveUserLoginPassword");
      if (this.checkLogin() && this.checkPasswords()){
        try {
          let user_data: IUserLogin = {
            login: this.currentUser.login,
            password: this.password1
          }
          let result_user = await UserService.createUser(
            user_data, this.authToken
          );
          console.log("result_user:", result_user);
          this.password1 = "";
          this.password2 = "";
          this.login_password_created = true;
          this.login_password_open_for_edit = false;

        } catch(e) {
          checkTokenExpired(e);
        }
      }
    },
    async sendCodeToEmail() {
      console.log("sendCodeToEmail")
    },
    async saveUserEmail() {
      console.log("saveUserEmail");
    },
    async sendCodeToTg() {
      console.log("sendCodeToTg");
    },
    async saveUserTgID() {
      console.log("saveUserTgID");
    },
    checkLogin(){
      return true;
    },
    checkPasswords(){
      if (this.password1 == this.password2){
        return true;
      } else {
        this.password2_mess = "passwords do not match";
        return false;
      }
    }
  },
  async mounted() {
    if (!this.authToken) {
      this.$router.push('/login');
    }
    console.log("before retrieve User");
    await this.retrieveUser();
    // this.currentUser.login = "test";
    if (this.currentUser.login){
      this.login_password_created = true;
    } else {
      this.login_password_created = false;
      this.login_password_open_for_edit = true;
    }
    // this.currentUser.email = "test";
    if (this.currentUser.email){
      this.email_linked = true;
    } else {
      this.email_linked = false;
      this.email_open_for_edit = true;
    }
    console.log("this.currentUser.tg_id: ", this.currentUser.tg_id);
    if (this.currentUser.tg_id){
      this.tg_linked = true;
    } else {
      this.tg_linked = false;
      this.tg_open_for_edit = true;
    }
  }
});
</script>
