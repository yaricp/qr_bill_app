import { createWebHistory, createRouter } from "vue-router";
import { RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    alias: "/main",
    name: "main",
    component: () => import("./pages/user/Main.vue"),
  },
  {
    path: "/qr_scanner",
    alias: "/qr_scanner",
    name: "qr_scanner",
    component: () => import("./components/QRScanner.vue"),
  },
  {
    path: "/goods_analytics",
    alias: "/goods_analytics",
    name: "goods_analytics",
    component: () => import("./pages/user/analytics/GoodsAnalytics.vue"),
  },
  {
    path: "/seller_analytics",
    alias: "/seller_analytics",
    name: "seller_analytics",
    component: () => import("./pages/user/analytics/SellerAnalytics.vue"),
  },
  {
    path: "/category_analytics/:by_months",
    alias: "/category_analytics",
    name: "category_analytics",
    component: () => import("./pages/user/analytics/CategoryAnalytics.vue"),
  },
  {
    path: "/bills/",
    name: "bills",
    component: () => import("./pages/user/lists/Bills.vue"),
  },
  {
    path: "/bill_detail/:id",
    name: "bill_detail",
    component: () => import("./pages/user/objects/BillDetail.vue"),
  },
  {
    path: "/goods/",
    name: "goods",
    component: () => import("./pages/user/lists/Goods.vue"),
  },
  {
    path: "/goods_detail/:id",
    name: "goods_detail",
    component: () => import("./pages/user/objects/GoodsDetail.vue"),
  },
  {
    path: "/categories",
    name: "categories",
    component: () => import("./pages/user/lists/Categories.vue"),
  },
  {
    path: "/category_products/",
    name: "category_products",
    component: () => import("./components/CategoryProduct.vue"),
  },
  {
    path: "/category_products/:bill_id",
    name: "category_products_bill_id",
    component: () => import("./components/CategoryProduct.vue"),
  },
  {
    path: "/logout",
    name: "logout",
    component: () => import("./pages/user/Logout.vue"),
  },
  {
    path: "/login/",
    name: "login",
    component: () => import("./pages/user/Login.vue"),
  },
  {
    path: "/login_by_tg/:link",
    name: "login_by_tg",
    component: () => import("./pages/user/LoginByTG.vue"),
  },
  {
    path: "/verify/:link",
    name: "verify_email_tg",
    component: () => import("./pages/user/VerifyEmailTG.vue"),
  },
  {
    path: "/register/",
    name: "register",
    component: () => import("./pages/user/Register.vue"),
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("./pages/user/Profile.vue"),
  }
];

// base: process.env.BASE_URL,

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const publicPages = [
    "/login/", "/login_by_tg/", "/register/", "/verify/"
  ];
  console.log("to.path", to.path)
  let authRequired = !publicPages.includes(to.path);
  
  const tokenStorage = localStorage.getItem('token');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (to.path.includes("/login_by_tg/")) {
    next();
  } else if (to.path.includes("/verify/")) {
    next();
  } else if (authRequired && !tokenStorage) {
    console.log("Redirect to login")
    next("/login/");
  } else {
    next();
  }
});

export default router;