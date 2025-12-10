import { createStore, Store as VuexStore } from 'vuex'

import { AuthModule, State as AuthState } from "./auth.module";

// define your typings for the store state
export type State = {
  auth: AuthState
}
export type Store = VuexStore<Pick<State, 'auth'>>

export const store = createStore<State>({
  modules: {
    auth: AuthModule,
  },
});

export function useStore () : Store {
  return store as Store
}

export default store