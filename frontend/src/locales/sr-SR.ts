import agreement_text from "@/locales/agreement/sr-SR"

export default {
  lang: {
    en: "English",
    ru: "Русский",
    sr: "Сrnogorski(Srpski)"
  },
  short_lang: "sr-SR",
  hello: "hello",
  yes: "yes",
  for: "za",
  install_btn: "Instaliraj QRacun",
  attantion: "Pažnja! Aplikacija je u fazi testiranja i zbog toga administracija ne snosi nikakvu odgovornost za čuvanje vaših podataka. Nastavljajući da koristite ovu aplikaciju, preuzimate sve rizike povezane sa gubitkom ili netačno obrađenim podacima.",
  agreement: {
    header: "Saglasnost za obradu ličnih podataka",
    register_text: "Za korišćenje ove aplikacije morate prihvatiti",
    register_link: "Saglasnost za obradu ličnih podatakaы",
    page: agreement_text
  },
  login: {
    header: "Stranica za prijavu",
    login: "Prijava",
    login_btn: "Prijava",
    password: "Lozinka",
    you_can_use: "Možete koristiti ovaj link ",
    to_login_link: " za generisanje linka za ulazak.",
    go_to_registration: "Ako nemate nalog, možete napraviti ",
    registration: "Registracija"
  },
  register: {
    header: "Registracija",
    login: "Prijava",
    password: "Lozinka",
    password2: "Ponovite lozinku",
    reg_btn: "Registracija",
    login_text: "Ako već imate nalog - ",
    login_link: "Stranica za prijavu"
  },
  main: {
    circle: {
      header: "Vaše kupovine po kategorijama za mjesec"
    },
    number_month: {
      header: "Vaši troškovi za mjesec"
    }
  },
  filter: {
    title: "Filter:",
    filter_names: {
      Seller: "po nazivu prodavca",
      Name: "po nazivu"
    }
  },
  menu: {
    scanner: "QR skener",
    cat_goods: "Kategorizuj svoje kupovine",
    cat_month_analytic: "Analitika po kategorijama za mjesec",
    analytics: {
      head: "Analitika",
      categories: "Po kategorijama",
      sellers: "Po prodavcima",
      goods: "Po proizvodima"
    },
    lists: {
      head: "Spiskovi",
      categories: "Kategorije",
      bills: "Računi",
      goods: "Proizvodi",
      sellers: "Prodavci"
    },
    user: {
      head: "Korisnik",
      profile: "Profil",
      logout: "Odjava"
    }
  },
  table: {
    fields:{
      Created: "Kreirano",
      Seller: "Prodavac",
      Summ: "Suma",
      Image: "Slika",
      ID: "ID",
      Quantity: "Količina",
      Unit: "Jedinica",
      Price: "Cijena",
      Name: "Naziv",
      Actions: "Akcije",
      Field: "Polje",
      Value: "Značenje"
    },
    first_column: {
      created: "Kreirano",
      value: "Značenje",
      payment_method: "Način plaćanja",
      seller: "Prodavac",
      goods_list: "Lista proizvoda",
      name: "Naziv",
      quantity: "Količina",
      unit_price_before_vat: "Jedinična cijena prije PDV-a",
      unit_price_after_vat: "Jedinična cijena nakon PDV-a",
      rebate: "Popust",
      rebate_reducing: "Umanjenje popusta",
      price_before_vat: "Cijena prije PDV-a",
      vat_rate: "Stopa PDV-a",
      vat_amount: "Iznos PDV-a",
      price_after_vat: "Cijena nakon PDV-a",
      unit: "Jedinica"
    }
  },
  profile: {
    main_header: "Korisnički profil",
    id: "Korisnički ID u sistemu",
    change_lang: "Promijeni jezik",
    login: {
      login: "Prijava",
      password: "Lozinka",
      password2: "Ponovi lozinku",
      btn_update: "Ažuriraj prijavu i/ili lozinku",
      btn_create: "Kreiraj prijavu i lozinku",
    },
    email: {
      email: "Email",
      btn_link_email: "Poveži email",
      btn_relink_email: "Ponovo poveži email",
      email_not_verified: "Nije potvrđen!"
    },
    tg: {
      tg_id: "Telegram ID",
      btn_link_tg: "Poveži Telegram",
      btn_relink_tg: "Ponovo poveži Telegram",
      tg_not_verified: "Nije potvrđen!"
    },
    dangerous: {
      confirm_header: "Da li ste sigurni da želite obrisati svoj nalog?",
      text1: "Da biste obrisali nalog, unesite svoj identifikator naloga",
      text2: "Imajte na umu da će nakon brisanja svi vaši zapisi o računima i kupovinama nestati. Oporavak naloga neće biti moguć.",
      header: "Opasna zona!",
      btn_open: "Otvori",
      btn_close: "Zatvori",
      delete_btn: "Obriši",
      cancel_btn: "Odrzucić",
      confirm_btn: "Potvrdi"
    },
    btn_change: "Promijeni",
    btn_close: "Zatvori",
    btn_verify: "Potvrdi"
  },
  scanner: {
    head: "QR skener",
    strings: {
      start_scan: "Započni skeniranje"
    },
    status: {
      1: "Izaberi kameru za skeniranje",
      2: "Skeniraj svoj račun sa QR kodom",
      3: "Slanje rezultata na server"
    },
    message: {
      wrong_url: "Pogrešan URL!",
      correct_url: "Pronađen ispravan URL",
      sent_to_server: "Uspješno poslato na server!"
    }
  },
  cat_goods: {
    head: {
      bill: "Nekategorisani artikli za račun sa ID-om",
      all: "Svi vaši nekategorisani artikli"
    },
    tip1: "Izaberite kategoriju za dole navedene artikle",
    tip2: "Kategorije",
    goods_list: "Lista proizvoda",
    filter: "Filter",
    show_other_cat: "Pokaži proizvode sa drugim kategorijama",
    check_uncheck_all: "Ozmarkiraj/Markiraj sve",
    btn_save: "Spasi kategoriju za odabrane artikle"
  },
  analytics: {
    cat: {
      header: {
        main: "Analitika proizvoda po kategorijama",
        by_count: "Količine proizvoda po kategorijama",
        by_summ: "Ukupna cijena proizvoda po kategorijama",
      },
      show_by_month: "Pokaži trenutni mjesec:",
      month: "Mjesec:",
      first_by_count: "Prvi po broju:",
      btn_update: "Ažuriraj",
      first_by_summ: "Prvi po sumi:",
      options: "Opcije",
      plot_count: {
        label: "Količine proizvoda po kategorijama"
      },
      plot_summ: {
        label: "Ukupna cijena proizvoda po kategorijama"
      }
    },
    goods: {
      header: {
        main: "Analitika proizvoda",
        by_count: "Količine proizvoda po nazivima",
        by_summ: "Ukupna cijena proizvoda po nazivima",
      },
      first_by_count: "Prvi po broju:",
      btn_update: "Ažuriraj",
      first_by_summ: "Prvi po sumi:",
      options: "Opcije",
      plot_count: {
        label: "Broj proizvoda po nazivu proizvoda"
      },
      plot_summ: {
        label: "Ukupna suma po nazivu proizvoda"
      }
    },
    sellers: {
      header: {
        main: "Analitika računa i dobara po prodavcima",
        by_count_bills: "Broj računa po prodavcima",
        by_summ_bills: "Ukupna cena računa po prodavcima",
        by_count_goods: "Ukupna količina dobara po prodavcima"
      },
      first_by_count: "Prvi od svih po broju:",
      btn_update: "Ažuriraj",
      first_by_summ: "Prvi od svih po sumi:",
      first_goods_by_summ: "Prvi od svih po broju dobara:",
      plot_count: {
        label: "Broj računa po imenu prodavaca"
      },
      plot_summ: {
        label: "Ukupna suma računa po imenu prodavaca"
      },
      plot_goods: {
        label: "Broj dobara po imenu prodavaca"
      }
    }
  },
  lists: {
    cat: {
      head: "Lista kategorija",
      empty_list_tip: "Kreirajte vlastite kategorije",
      add_cat_placeholder: "Ime nove kategorije",
      btn_add: "Dodaj",
      btn_del: "Obriši",
      btn_edit: "Izmeni",
      btn_save: "Spasi"
    },
    goods: {
      head: "Lista dobara"
    },
    bills: {
      head: "Lista računa"
    }
  },
  objects: {
    bill: {
      head: "Detalji računa",
      btn_cat_goods: "Kategorizujte dobra ovog računa"
    },
    goods: {
      head: "Detalji stavke računa",
      cats: "Kategorije",
      btn_save: "Spasi"
    }
  },
  month: {
    1: "Januar",
    2: "Februar",
    3: "Mart",
    4: "April",
    5: "Maj",
    6: "Jun",
    7: "Jul",
    8: "Avgust",
    9: "Septembar",
    10: "Oktobar",
    11: "Novembar",
    12: "Decembar"
  }
}



