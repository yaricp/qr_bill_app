export default {
  lang: {
    en: "English",
    ru: "Русский",
    sr: "Сrnogorski(Srpski)"
  },
  change_lang: "Change language",
  short_lang: "en-US",
  hello: "hello",
  yes: "yes",
  for: "for",
  install_btn: "Install QRacun",
  agreement: {
    header: "License and Agreements",
    register_text: "For use this application you need accept ",
    register_link: "License and Agreement"
  },
  login: {
    header: "Login Page",
    login: "Login",
    login_btn: "Enter",
    password: "Password",
    you_can_use: "You can use this link ",
    to_login_link: " to generate link to enter.",
    go_to_registration: "If you don't have account you can make ",
    registration: "Registration"
  },
  register: {
    header: "Registration",
    login: "Login",
    password: "Password",
    password2: "Repeat password",
    reg_btn: "Registration",
    login_text: "If you have account already - ",
    login_link: "Login Page"
  },
  main: {
    circle: {
      header: "Your purchases by categories for month"
    },
    number_month: {
      header: "Your expenses for the month"
    }
  },
  filter: {
    title: "Filter:",
    filter_names: {
      Seller: "by name of seller",
      Name: "by name"
    }
  },
  menu: {
    scanner: "QR Scanner",
    cat_goods: "Categorize your goods",
    cat_month_analytic: "Analytics by Categories for month",
    analytics: {
      head: "Analytics",
      categories: "By Categories",
      sellers: "By Sellers",
      goods: "By Goods"
    },
    lists: {
      head: "Lists",
      categories: "Categories",
      bills: "Bills",
      goods: "Goods",
      sellers: "Sellres"
    },
    user: {
      head: "User",
      profile: "Profile",
      logout: "Logout"
    }
  },
  table: {
    fields:{
      Created: "Created",
      Seller: "Seller",
      Summ: "Summ",
      Image: "Image",
      ID: "ID",
      Quantity: "Quantity",
      Unit: "Unit",
      Price: "Price",
      Name: "Name",
      Actions: "Actions",
      Field: "Field",
      Value: "Value"
    },
    first_column: {
      created: "created",
      value: "value",
      payment_method: "payment method",
      seller: "seller",
      goods_list: "goods list",
      name: "name",
      quantity: "quantity",
      unit_price_before_vat: "unit price before vat",
      unit_price_after_vat: "unit price after vat",
      rebate: "rebate",
      rebate_reducing: "rebate reducing",
      price_before_vat: "price before vat",
      vat_rate: "vat rate",
      vat_amount: "vat amount",
      price_after_vat: "price after vat",
      unit: "unit"
    }
  },
  profile: {
    main_header: "User Profile",
    id: "User ID in system",
    change_lang: "Change language",
    login:{
      login: "Login",
      password: "Password",
      password2: "Repeat password",
      btn_update: "Update Login and/or password",
      btn_create: "Create Login and password",
    },
    email: {
      email: "Email",
      btn_link_email: "Link Email",
      btn_relink_email: "Relink Email",
      email_not_verified: "Not verified!"
    },
    tg: {
      tg_id: "Telegram ID",
      btn_link_tg: "Link Telegram",
      btn_relink_tg: "Relink Telegram",
      tg_not_verified: "Not verified!"
    },
    dangerous: {
      confirm_header: "Are you sure you want delete your account?",
      text1: "For deleting your account enter your ID account",
      text2: "Please note that after deletion all your records of bills and purchases will disappear. It will be impossible to restore the account",
      header: "Dangerous zone!",
      btn_open: "Open",
      btn_close: "Close",
      delete_btn: "Delete",
      cancel_btn: "Cancel",
      confirm_btn: "Confirm"
    },
    btn_change: "Change",
    btn_close: "Close",
    btn_verify: "Verify"
  },
  scanner: {
    head: "QR Scanner",
    strings: {
      start_scan: "Start Scan"
    },
    status: {
      1: "Choose camera for scanning",
      2: "Scan you bill with QR code",
      3: "Sending result to server"
    },
    message: {
      wrong_url: "Wrong URL!",
      correct_url: "Found Correct URL",
      sent_to_server: "sent to server successful!"
    }
  },
  cat_goods: {
    head: {
      bill: "Uncategorized items for bill with ID",
      all: "All your uncategorized items"
    },
    tip1: "Choose category for items below",
    tip2: "Categories",
    goods_list: "Goods List",
    filter: "Filter",
    show_other_cat: "Show goods with other categories",
    check_uncheck_all: "Check/Uncheck All",
    btn_save: "Save category for selected items"
  },
  analytics: {
    cat: {
      header: {
        main: "Analytics Goods by categories",
        by_count: "Quantities goods by categories",
        by_summ: "Total price goods by categories",
      },
      show_by_month: "Show current month:",
      month: "Month:",
      first_by_count: "First from all by count:",
      btn_update: "Update",
      first_by_summ: "First from all by summ:",
      options: "Options",
      plot_count: {
        label: "Quantities goods by categories"
      },
      plot_summ: {
        label: "Total price goods by categories"
      }
    },
    goods: {
      header: {
        main: "Analytics Goods",
        by_count: "Quantities goods by names",
        by_summ: "Total price goods by names",
      },
      first_by_count: "First from all by count:",
      btn_update: "Update",
      first_by_summ: "First from all by summ:",
      options: "Options",
      plot_count: {
        label: "Number of goods by name of goods"
      },
      plot_summ: {
        label: "Total of sum by name of goods"
      }
    },
    sellers: {
      header: {
        main: "Analytics Bills and Goods by Sellers",
        by_count_bills: "Count bills by sellers",
        by_summ_bills: "Total price bills by sellers",
        by_count_goods: "Total quantity goods by sellers"
      },
      first_by_count: "First from all by count:",
      btn_update: "Update",
      first_by_summ: "First from all by summ:",
      first_goods_by_summ: "First from all by count goods:",
      plot_count: {
        label: "Number of bills by name of sellers"
      },
      plot_summ: {
        label: "Total sum of bills By name of Sellers"
      },
      plot_goods: {
        label: "Number of goods by name of sellers"
      }
    }
  },
  lists: {
    cat: {
      head: "Categories List",
      empty_list_tip: "Create your own categories",
      add_cat_placeholder: "name of a new category",
      btn_add: "Add",
      btn_del: "Delete",
      btn_edit: "Edit",
      btn_save: "Save"
    },
    goods: {
      head: "Goods List"
    },
    bills: {
      head: "Bills List"
    }
  },
  objects: {
    bill: {
      head: "Bill Details",
      btn_cat_goods: "Categorize goods this bill"
    },
    goods: {
      head: "Bill Item Details",
      cats: "Categories",
      btn_save: "Save"
    }
  },
  month: {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
  }
}