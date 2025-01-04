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
  {
    path: "/login",
    name: "login",
    component: () => import("./components/user/Login.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("./components/user/Register.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    // lazy-loaded
    component: () => import("./components/user/Profile.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/home'];
  const authRequired = !publicPages.includes(to.path);
  const tokenStorage = localStorage.getItem('token');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !tokenStorage) {
    console.log("Redirect to login")
    next('/login');
  } else {
    next();
  }
});

export default router;