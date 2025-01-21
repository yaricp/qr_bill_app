import {
  ActionContext,
  ActionTree,
  GetterTree,
  MutationTree,
  Module,
  Store as VuexStore,
  CommitOptions,
  DispatchOptions,
} from 'vuex';

import { State as RootState } from '@/store';

import AuthService from '@/services/auth';
import UserService from '@/services/users';
// import { IUserLogin } from "@/interfaces/users";

// Declare state
export type State = {
  loggedIn: boolean;
  token: string;
  lang: string;
}

// Create initial state

let token;
let local_db_token = localStorage.getItem('token');

if (local_db_token){
  token = JSON.parse(local_db_token);
}
let lang = "en";
let local_db_lang = localStorage.getItem('lang');

if (local_db_lang){
  lang = JSON.parse(local_db_lang);
}

export const initialState = token
  ? { loggedIn: true , token, lang }
  : { loggedIn: false , token: "", lang };

const state: State = initialState;

// Setup store type
// export type Store<S = State> = Omit<
//   VuexStore<S>,
//   'commit' | 'getters' | 'dispatch'
// > & {
//   commit<K extends keyof Mutations, P extends Parameters<Mutations[K]>[1]>(
//     key: K,
//     payload: P,
//     options?: CommitOptions,
//   ): ReturnType<Mutations[K]>
// } & {
//   getters: {
//     [K in keyof Getters]: ReturnType<Getters[K]>
//   }
// } & {
//   dispatch<K extends keyof Actions>(
//     key: K,
//     payload: Parameters<Actions[K]>[1],
//     options?: DispatchOptions,
//   ): ReturnType<Actions[K]>
// }

export const AuthModule: Module<State, RootState> = {
  namespaced: true,
  state,
  actions: {
    async login({ commit }, user) {
      try {
        let response = await AuthService.login(user);
        console.log('loginSuccess');
        console.log('response.data:', response.data);
        if (response.data && response.data.access_token){
          let token = response.data.access_token;
          console.log("save to localStorage");
          localStorage.setItem(
            'token', JSON.stringify(token)
          );
          console.log("commit to loginSuccess");
          commit('loginSuccess', token);
          response = await UserService.getUserProfile(token);
          console.log('getUserProfile response.data:', response.data);
          let lang = response.data.lang;
          console.log("commit to save lang");
          commit('langCommit', lang);
        } else {
          console.log("commit loginFailure: ");
          commit('loginFailure');
        }
      } catch(e: any) {
        console.log("err:", e);
        if(e.status == 401){
          return 401;
        }
        console.log("commit loginFailure: ", e);
        commit('loginFailure');
      }
    },
    async login_by_tg({ commit }, link) {
      try {
        let token = await AuthService.login_by_tg(link);
        console.log('loginSuccess');
        console.log('token:', token);
        if (token){
          console.log("save to localStorage");
          localStorage.setItem(
            'token', JSON.stringify(token)
          );
          console.log("commit to loginSuccess");
          commit('loginSuccess', token);
        }
      } catch(e) {
        console.log("err:", e);
        console.log("commit loginFailure: ", e);
        commit('loginFailure');
      }
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user) {
      return AuthService.register(user).then(
        response => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('registerFailure');
          return Promise.reject(error);
        }
      );
    },
    async change_lang({ commit }, lang) {
      try {
        console.log("lang: ", lang);
        let user_profile = {
          lang: lang
        }
        let response  = await UserService.updateUserProfile(
          user_profile,
          state.token
        )
        if (response.status == 200 && response.data) {
          let lang = response.data.lang;
          console.log("commit to save lang");
          commit('langCommit', lang);
        } else {
          console.log("Something wrong with saving user profile");
        }

      } catch(e) {
        console.log("Error:", e);
      }
    }
  },
  mutations: {
    loginSuccess(state, token) {
      state.loggedIn = true;
      state.token = token;
    },
    langCommit(state, lang) {
      console.log("save lang to localStorage");
      localStorage.setItem(
        'lang', JSON.stringify(lang)
      );
      state.lang = lang;
    },
    loginFailure(state) {
      state.loggedIn = false;
      state.token = "";
    },
    logout(state) {
      state.loggedIn = false;
      state.token = "";
    },
    registerSuccess(state) {
      state.loggedIn = false;
    },
    registerFailure(state) {
      state.loggedIn = false;
    }
  }
};