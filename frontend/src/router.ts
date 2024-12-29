import { createWebHistory, createRouter } from "vue-router";
import { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    alias: "/analytics",
    name: "analytics",
    component: () => import("./components/Analytics.vue"),
  },
  {
    path: "/goods/",
    alias: "/goods",
    name: "goods",
    component: () => import("./components/GoodsList.vue"),
  },
  {
    path: "/goods/:id",
    name: "goods-details",
    component: () => import("./components/GoodsDetails.vue"),
  },
  {
    path: "/goods/add",
    name: "add",
    component: () => import("./components/GoodsAdd.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;