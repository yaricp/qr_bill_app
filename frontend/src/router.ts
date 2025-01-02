import { createWebHistory, createRouter } from "vue-router";
import { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    alias: "/goods_analytics",
    name: "goods_analytics",
    component: () => import("./components/GoodsAnalytics.vue"),
  },
  {
    path: "/qr_scanner",
    alias: "/qr_scanner",
    name: "qr_scanner",
    component: () => import("./components/QRScanner.vue"),
  },
  {
    path: "/seller_analytics",
    alias: "/seller_analytics",
    name: "seller_analytics",
    component: () => import("./components/SellerAnalytics.vue"),
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