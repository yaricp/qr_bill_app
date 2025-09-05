import { createApp } from 'vue';
import App from './App.vue';
import router from "@/router";
import { store } from "./store";
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/main.css';
import { FontAwesomeIcon } from './plugins/font-awesome';
import i18n from './plugins/i18n';
import './registerServiceWorker';


createApp(App)
.use(router)
.use(store)
.use(i18n)
.component("font-awesome-icon", FontAwesomeIcon)
.mount("#app");


