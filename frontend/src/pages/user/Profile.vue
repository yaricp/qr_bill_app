<template>
    <div class="container" v-if="currentUser">
      <div class="row">
        <header class="jumbotron">
          <h3>
            {{ $t("profile.main_header") }}
          </h3>
        </header>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col">
          <strong>{{ $t('profile.change_lang')}}</strong>
        </div>
        <div class="col">
          <div class="locale-changer">
            <select 
              v-model="$i18n.locale"
              @change="langChanged()"
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
        <hr/>
      </div>
      <div class="row">
        <div class="col"><strong>{{ $t("profile.id") }}:</strong></div>
        <div class="col">{{ currentUser.id }}</div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col">
          <strong>{{ $t("profile.login.login") }}:</strong>
        </div>
        <div class="col">
          <span 
            v-if="login_password_created && !login_password_open_for_edit"
          >{{ currentUser.login }}</span>
          <span v-if="login_password_open_for_edit">
            <input type="text" v-model="currentUser.login">
          </span>
        </div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="!login_password_open_for_edit"
            @click="login_password_open_for_edit =!login_password_open_for_edit"
          >
            {{ $t("profile.btn_change") }}
          </button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="login_password_created && login_password_open_for_edit"
            @click="login_password_open_for_edit =!login_password_open_for_edit"
          >
            {{ $t("profile.btn_close") }}
          </button>
        </div>
      </div>
      <div class="row" v-if="login_password_open_for_edit">
        <div class="col"></div>
        <div class="col">{{ login_mess }}</div>
        <div class="col"></div>
      </div>
      <div class="row" v-if="login_password_open_for_edit">
        <div class="col">
          <strong>{{ $t("profile.login.password") }}:</strong>
        </div>
        <div class="col">
          <span>
            <input type="password" v-model="password1">
          </span>
        </div>
        <div class="col"></div>
      </div>
      <div class="row" v-if="login_password_open_for_edit">
        <div class="col"></div>
        <div class="col">{{ password1_mess }}</div>
        <div class="col"></div>
      </div>
      <div class="row" v-if="login_password_open_for_edit">
        <div class="col">
          <strong>{{ $t("profile.login.password2") }}:</strong>
        </div>
        <div class="col">
          <span>
            <input type="password" v-model="password2">
          </span>
        </div>
        <div class="col"></div>
      </div>
      <div class="row" v-if="login_password_open_for_edit">
        <div class="col"></div>
        <div class="col">{{ password2_mess }}</div>
        <div class="col"></div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button 
            class="btn btn-outline-secondary"
            type="button"
            v-if="login_password_open_for_edit"
            @click="saveUserLoginPassword"
          >
            {{ login_btn_text }}
          </button>
        </div>
        <div class="col"></div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col">
          <strong>{{ $t("profile.email.email") }}:</strong>
        </div>
        <div class="col">
          <span v-if="email_linked && !email_open_for_edit"> {{ currentUser.email }} </span>
          <span v-if="email_open_for_edit">
            <input
              type="text"
              v-model="currentUser.email"
              @keyup="checkEmail"
            >
          </span> &nbsp;&nbsp;
          <span 
            v-if="currentUser.email_verified"
            style="color: green;"
            :title="$t('profile.email.verified')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16">
              <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
            </svg>
          </span>
          <span 
            v-if="!currentUser.email_verified"
            style="color: red;"
            :title="$t('profile.email.not_verified')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle" viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
              <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
            </svg>
          </span>
          <span>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="email_verify_btn_showed" 
              @click="confirmEmail"
            >
            {{ $t("profile.btn_verify") }}
            </button>
          </span> 
        </div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="email_linked && !email_open_for_edit"
            @click="email_open_for_edit =!email_open_for_edit"
          >
            {{ $t("profile.btn_change") }}
          </button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="email_linked && email_open_for_edit"
            @click="email_open_for_edit =!email_open_for_edit"
          >
            {{ $t("profile.btn_close") }}
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ email_mess }}</div>
        <div class="col"></div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="email_open_for_edit"
            @click="saveUserEmail"
          >{{ email_btn_text }}</button>
        </div>
        <div class="col"></div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col">
          <strong>{{ $t("profile.tg.tg_id") }}:</strong>
        </div>
        <div class="col">
          <span v-if="tg_linked && !tg_open_for_edit"> {{ currentUser.tg_id }} </span>
          <span v-if="tg_open_for_edit">
            <input 
              type="text"
              v-model="currentUser.tg_id"
              @keyup="checkTG"
            >
          </span>
          &nbsp;&nbsp;
          <span 
            v-if="currentUser.tg_verified"
            style="color: green;"
            :title="$t('profile.tg.verified')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check-lg" viewBox="0 0 16 16">
              <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
            </svg>
          </span>
          <span 
            v-if="!currentUser.tg_verified"
            style="color: red;"
            :title="$t('profile.tg.not_verified')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle" viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
              <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
            </svg>
          </span>
          <span>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="tg_verify_btn_showed" 
              @click="confirmTG"
            >
            {{ $t("profile.btn_verify") }}
            </button>
          </span> 
        </div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="!tg_open_for_edit" 
            @click="tg_open_for_edit =!tg_open_for_edit"
          >
            {{ $t("profile.btn_change") }}
          </button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="tg_linked && tg_open_for_edit" 
            @click="tg_open_for_edit =!tg_open_for_edit"
          >
            {{ $t("profile.btn_close") }}
          </button>
        </div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">{{ tg_mess }}</div>
        <div class="col"></div>
      </div>
      <div class="row">
        <div class="col"></div>
        <div class="col">
          <button 
            class="btn btn-outline-secondary"
            type="button"
            v-if="tg_open_for_edit"
            @click="saveUserTgID"
          >
            {{ tg_btn_text }}
          </button>
        </div>
        <div class="col"></div>
      </div>
      <div class="row">
        <hr/>
      </div>
      <div class="row">
        <div class="col"> {{ $t("profile.dangerous.header")}}</div>
        <div class="col">
          
        </div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="!dangerous_zone_open"
            @click="dangerous_zone_open =!dangerous_zone_open"
          >
            {{ $t("profile.dangerous.btn_open") }}
          </button>
          <button
            class="btn btn-outline-secondary"
            type="button"
            v-if="dangerous_zone_open"
            @click="dangerous_zone_open =!dangerous_zone_open"
          >
            {{ $t("profile.dangerous.btn_close") }}
          </button>
        </div>
      </div>
      <div class="row" v-if="dangerous_zone_open">
        <div class="col"> {{ $t("profile.dangerous.text")}}</div>
        <div class="col">
          <input type="text"/>
        </div>
        <div class="col">
          
        </div>
      </div>
      <div class="row" v-if="dangerous_zone_open">
        <div class="col"> {{ $t("profile.dangerous.text")}}</div>
        <div class="col">
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="deleteAccount"
          >{{ $t("profile.dangerous.delete")}}</button>
        </div>
        <div class="col">
        </div>
      </div>
      <div class="row">
        <hr/>
      </div>
    </div>
    
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import UserService from "@/services/users";
import AuthService from "@/services/auth";
import { IUser, IUserLogin } from "@/interfaces/users";
import { useStore } from '@/store';
import { checkTokenExpired } from "@/http-common";

export default defineComponent({
  name: 'profile-page',
  data() {
    return {
      currentUser: {} as IUser,
      login_mess: "" as string,
      login_btn_text: "" as string,
      password1: "" as string,
      password1_mess: "" as string,
      password2: "" as string,
      password2_mess: "" as string,
      login_password_created: false as boolean,
      login_password_open_for_edit: false as boolean,
      saved_email: "" as string,
      email_linked: false as boolean,
      email_btn_text: "" as string,
      message_verify_email_sent: false as boolean,
      email_mess: "" as string,
      email_open_for_edit: false as boolean,
      email_verify_btn_showed: false as boolean,
      saved_tg_id: 0 as number,
      tg_linked: false as boolean,
      tg_btn_text: "" as string,
      tg_verify_email_sent: false as boolean,
      tg_mess: "" as string,
      tg_open_for_edit: false as boolean,
      tg_verify_btn_showed: false as boolean,
      dangerous_zone_open: false as boolean
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
    prepareButtonsAndLabels() {
      let link_email_exists;
      let link_tg_exists;
      if (this.currentUser.login){
        this.login_password_created = true;
        this.login_btn_text = this.$t("profile.login.btn_update");
      } else {
        this.login_password_created = false;
        this.login_password_open_for_edit = true;
        this.login_btn_text = this.$t("profile.login.btn_create");
      }
      link_email_exists = this.currentUser.links.filter(
        (item) => {return item.link_for == "email"}
      )[0];
      link_tg_exists = this.currentUser.links.filter(
        (item) => {return item.link_for == "tg"}
      )[0];
      if (this.currentUser.email){
        this.saved_email = this.currentUser.email;
        this.email_linked = true;
        this.email_btn_text = this.$t("profile.email.btn_relink_email");
        console.log(
          "this.currentUser.email_verified: ",
          this.currentUser.email_verified
        );
        if (!this.currentUser.email_verified) {
          console.log("email.not_verified");
          this.email_mess = "";
          // this.email_mess = this.$t("profile.email.not_verified")
        }
      } else {
        this.email_linked = false;
        this.email_open_for_edit = true;
        this.email_btn_text = this.$t("profile.email.btn_link_email");
      } 
      console.log("this.currentUser.tg_id: ", this.currentUser.tg_id);
      if (this.currentUser.tg_id){
        this.tg_linked = true;
        this.saved_tg_id = this.currentUser.tg_id;
        this.tg_btn_text = this.$t("profile.tg.btn_relink_tg");
        if (!this.currentUser.tg_verified) {
          console.log("tg.not_verified");
          this.tg_mess = "";
          // this.tg_mess = this.$t("profile.tg.not_verified")
        }
      } else {
        this.tg_linked = false;
        this.tg_open_for_edit = true;
        this.tg_btn_text = this.$t("profile.tg.btn_link_tg");
      }
      if (this.email_linked){
        if (link_email_exists){
          this.email_verify_btn_showed = false;
          this.email_mess = this.$t("profile.email.check_your_email");
        } else if (!this.currentUser.email_verified) {
          this.email_verify_btn_showed = true;
        } else {
          console.log("Email verified!");
          this.email_mess = "";
          // this.email_mess = this.$t("profile.email.verified")
        }
      } else {
        this.email_verify_btn_showed = false;
      }
      
      if (this.tg_linked){
        if (link_tg_exists){
          this.tg_verify_btn_showed = false;
          this.tg_mess = this.$t("profile.tg.check_your_email");
        } else if (!this.currentUser.tg_verified) {
          this.tg_verify_btn_showed = true;
        } else {
          console.log("tg verified");
          this.tg_mess = "";
          // this.tg_mess = this.$t("profile.tg.verified")
        }
      } else {
        this.tg_verify_btn_showed = false;
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
          this.prepareButtonsAndLabels();
        } catch(e) {
          checkTokenExpired(e);
        }
      }
    },
    async saveUserEmail() {
      console.log("saveUserEmail");
      let user_profile = {
        "email": this.currentUser.email
      }
      try {
        let response = await UserService.updateUserProfile(
          user_profile, this.authToken
        );
        console.log("response.data: ", response.data);
        this.currentUser = response.data;
        this.email_open_for_edit = false;
        this.prepareButtonsAndLabels();
      } catch(e) {
        console.log("Error: ", e);
      }
    },
    async saveUserTgID() {
      console.log("saveUserTgID");
      let tg_id = 0;
      if (this.currentUser.tg_id){
        tg_id = this.currentUser.tg_id;
      }
      let user_profile = {"tg_id": tg_id};
      try {
        let response = await UserService.updateUserProfile(
          user_profile, this.authToken
        );
        console.log("response.data: ", response.data);
        this.currentUser = response.data;
        this.tg_open_for_edit = false;
        this.prepareButtonsAndLabels();
      } catch(e) {
        console.log("Error: ", e);
      }
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
    }, 
    checkEmail(){
      if (this.currentUser.email != this.saved_email){
        this.email_linked = false;
        this.email_mess = "";
        this.email_verify_btn_showed = false;
      }
    },
    checkTG(){
      if (this.currentUser.tg_id != this.saved_tg_id){
        this.tg_linked = false;
        this.tg_mess = "";
        this.tg_verify_btn_showed = false;
      }
    },
    async langChanged(){
      let lang  = this.$i18n.locale;
      let user_profile = {
        id: this.currentUser.id,
        lang: lang,
        token: this.authToken
      }
      let result = await this.$store.dispatch(
        "auth/change_lang", lang
      );

    },
    async confirmTG() {
      try {
        let request = await AuthService.sendVerifyLinkToTG(
          this.currentUser.tg_id, this.authToken
        )
        this.currentUser = request.data;
        this.prepareButtonsAndLabels();
      } catch(err) {
        console.log("Error: ", err)
      }
    },
    async confirmEmail() {
      try {
        let request = await AuthService.sendVerifyLinkToEmail(
          this.currentUser.email, this.authToken
        )
        this.currentUser = request.data;
        this.prepareButtonsAndLabels();
      } catch(err) {
        console.log("Error: ", err)
      }
    },
    async deleteAccount(){
      console.log("Delete Account!");
    }
  },
  async mounted() {
    if (!this.authToken) {
      this.$router.push('/login');
    }
    console.log("before retrieve User");
    await this.retrieveUser();
    this.prepareButtonsAndLabels();
    
    
  }
});
</script>
