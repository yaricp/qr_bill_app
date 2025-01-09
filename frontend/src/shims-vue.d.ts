import VueRouter, { Route } from 'vue-router'

/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// declare module '*.vue' {
//   import Vue from 'vue';
//   export default Vue;
// }

declare module 'vue/types/vue' {
  interface Vue {
    $router: VueRouter
  }
}

declare module '@j-t-mcc/vue3-chartjs'

declare module 'bootstrap/dist/js/bootstrap.bundle'