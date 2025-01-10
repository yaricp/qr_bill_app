import { createWebHistory, createRouter } from "vue-router";
import { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    alias: "/goods_analytics",
    name: "goods_analytics",
    component: () => import("./components/analytics/GoodsAnalytics.vue"),
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
    component: () => import("./components/analytics/SellerAnalytics.vue"),
  },
  {
    path: "/category_analytics",
    alias: "/category_analytics",
    name: "category_analytics",
    component: () => import("./components/analytics/CategoryAnalytics.vue"),
  },
  {
    path: "/bills/",
    name: "bills",
    component: () => import("./components/list_objects/Bills.vue"),
  },
  {
    path: "/goods/",
    name: "goods",
    component: () => import("./components/list_objects/Goods.vue"),
  },
  {
    path: "/goods_detail/:goods_id",
    name: "goods_detail",
    component: () => import("./components/objects/GoodsDetail.vue"),
  },
  {
    path: "/categories",
    name: "categories",
    component: () => import("./components/list_objects/Categories.vue"),
  },
  {
    path: "/category_goods/:bill_id",
    name: "category_goods_bill_id",
    component: () => import("./components/CategoryGoods.vue"),
  },
  {
    path: "/category_goods",
    name: "category_goods",
    component: () => import("./components/CategoryGoods.vue"),
  },
  {
    path: "/logout",
    name: "logout",
    component: () => import("./components/user/Logout.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("./components/user/Login.vue"),
  },
  {
    path: "/login_by_tg/:link",
    name: "login_by_tg",
    component: () => import("./components/user/LoginByTG.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("./components/user/Register.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("./components/user/Profile.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const publicPages = [
    '/login', '/login_by_tg/', '/register', '/home'
  ];
  console.log("to.path", to.path)
  let authRequired = !publicPages.includes(to.path);
  
  const tokenStorage = localStorage.getItem('token');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (to.path.includes("/login_by_tg/")) {
    next();
  } else if (authRequired && !tokenStorage) {
    console.log("Redirect to login")
    next('/login');
  } else {
    next();
  }
});

export default router;