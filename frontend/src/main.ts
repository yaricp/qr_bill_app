import { createApp } from 'vue';
import App from './App.vue';
import router from "@/router";
import { store } from "./store";
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
// import * as bootstrap from 'bootstrap/dist/js/bootstrap.bundle';
import './assets/main.css';
import { FontAwesomeIcon } from './plugins/font-awesome';
// import AddToHomescreen from '@owliehq/vue-addtohomescreen';
import './registerServiceWorker';


createApp(App)
.use(router)
.use(store)
.component("font-awesome-icon", FontAwesomeIcon)
.mount("#app");

// .provide('bootstrap', bootstrap)
// .use(AddToHomescreen, {
//     buttonColor: 'blue',
// })

