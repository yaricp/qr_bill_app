export default {
  lang: {
    en: "English",
    ru: "Русский",
    sr: "Српски"
  },
  short_lang: "ru-RU",
  hello: "привет",
  yes: "да",
  for: "за",
  install_btn: "Установить QRacun",
  main: {
    circle: {
      header: "Твои покупки по категориям за месяц"
    },
    number_month: {
      header: "Ваши расходы за месяц"
    }
  },
  filter: {
    title: "Фильтр:",
    filter_names: {
      Seller: "по названию продавца",
      Name: " по названию"
    }
  },
  menu: {
    scanner: "QR Сканер",
    cat_goods: "Категоризуй свои покупки",
    cat_month_analytic: "Аналитика по категориям за месяц",
    analytics: {
      head: "Аналитика",
      categories: "По категориям",
      sellers: "По продавцам",
      goods: "По товарам"
    },
    lists: {
      head: "Списки",
      categories: "Категории",
      bills: "Счета",
      goods: "Товары",
      sellers: "Продавцы"
    },
    user: {
      head: "Пользователь",
      profile: "Профиль",
      logout: "Выход"
    }
  },
  table: {
    fields:{
      Created: "Дата создания",
      Seller: "Продавец",
      Summ: "Общая сумма",
      Image: "Фото",
      ID: "ID",
      Quantity: "Количество",
      Unit: "Единица измерения",
      Price: "Цена",
      Name: "Наименование",
      Actions: "Действия",
      Field: "Поле",
      Value: "Значение"
    },
    first_column: {
      created: "создан",
      value: "сумма",
      payment_method: "метод оплаты",
      seller: "продавец",
      goods_list: "список товаров",
      name: "наименование",
      quantity: "количество",
      unit_price_before_vat: "цена за единицу до НДС",
      unit_price_after_vat: "цена за единицу после НДС",
      rebate: "скидка",
      rebate_reducing: "применение скидки",
      price_before_vat: "цена до НДС",
      vat_rate: "ставка НДС",
      vat_amount: "сумма НДС",
      price_after_vat: "цена после НДС",
      unit: "единица"
    }
  },
  profile: {
    main_header: "Профиль Пользователя",
    id: "Идентификатор пользователя в системе",
    login: "Логин",
    password: "Пароль",
    password2: "Повторите пароль",
    change_lang: "Сменить язык",
    btn_update: "Обновить логин и/или пароль",
    btn_create: "Cоздать Логин и пароль",
    email: "Email",
    btn_link_email: "Привязать Email",
    btn_relink_email: "Перепривязать Email",
    tg_id: "Телеграм ID",
    btn_change: "Изменить",
    btn_close: "Закрыть",
    btn_link_tg: "Привязать Телеграм",
    btn_relink_tg: "Перепривязать Телеграм"
  },
  scanner: {
    head: "QR Сканнер",
    strings: {
      start_scan: "Старт сканирования"
    },
    status: {
      1: "Выберите камеру для сканирования",
      2: "Отсканируйте QR-код на чеке",
      3: "Отсылаем данные на сервер"
    },
    message: {
      wrong_url: "Не верные данные в QR!",
      correct_url: "Данные QR верны",
      sent_to_server: "Данные успешно отправлены на сервер!"
    }
  },
  cat_goods: {
    head: {
      bill: "Товары вне категорий для счета с ID",
      all: "Все товары без категорий"
    },
    tip1: "Выберите категорию для товаров в списке ниже",
    tip2: "Категории",
    goods_list: "Список товаров",
    filter: "Фильтр по названию",
    show_other_cat: "Показать товары с другой категорией",
    check_uncheck_all: "Выделить все/Убрать выделение для всех",
    btn_save: "Сохранить товары в выбранной категории"
  },
  analytics: {
    cat: {
      header: {
        main: "Аналитика товаров по категориям",
        by_count: "Единиц товаров по категориям",
        by_summ: "Общие затраты по категориям",
      },
      show_by_month: "Показать за текущий месяц:",
      month: "Месяц:",
      first_by_count: "Показать первые по количеству:",
      btn_update: "Обновить",
      first_by_summ: "Показать первые по сумме:",
      options: "Опции",
      plot_count: {
        label: "Количество товаров по категориям"
      },
      plot_summ: {
        label: "Общая стоимость товаров по категориям"
      }
    },
    goods: {
      header: {
        main: "Аналитика товаров",
        by_count: "Единиц товаров по названиям",
        by_summ: "Общие затраты по названиям",
      },
      first_by_count: "Показать первые по количеству:",
      btn_update: "Обновить",
      first_by_summ: "Показать первые по сумме:",
      options: "Опции",
      plot_count: {
        label: "Количество купленных товаром по именам"
      },
      plot_summ: {
        label: "Затраты на товары по именам"
      }
    },
    sellers: {
      header: {
        main: "Аналитика счетов и товаров по продавцам",
        by_count_bills: "Количество счетов по продавцам",
        by_summ_bills: "Сумма счетов по продавцам",
        by_count_goods: "Количество товаров по продавцам"
      },
      first_by_count: "Показать первые по количеству:",
      btn_update: "Обновить",
      first_by_summ: "Показать первые по сумме:",
      first_goods_by_summ: "Показать первые по количеству товаров:",
      plot_count: {
        label: "Количество счетов по именам продавцов"
      },
      plot_summ: {
        label: "Общая сумма счетов по именам продавцов"
      },
      plot_goods: {
        label: "Количество товаров по именам продавцов"
      }
    }
  },
  lists: {
    cat: {
      head: "Список категорий",
      empty_list_tip: "Создай свои категории",
      add_cat_placeholder: "название новой категории",
      btn_add: "Добавить",
      btn_del: "Удалить",
      btn_edit: "Изменить",
      btn_save: "Сохранить"
    },
    goods: {
      head: "Список товаров"
    },
    bills: {
      head: "Список счетов"
    }
  },
  objects: {
    bill: {
      head: "Детали счета",
      btn_cat_goods: "Категоризуй товары этого счета"
    },
    goods: {
      head: "Детали позиции в счете",
      cats: "Категории",
      btn_save: "Сохранить"
    }
  },
  month: {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
  }
}