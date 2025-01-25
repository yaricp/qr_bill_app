<template>
  <div class="row">
    <div class="col-md-12">
      <h3>{{ main_header }}</h3>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <div class="input-group mb-3">
        <p>{{ $t("cat_goods.tip1") }}</p>
      </div>
      <div class="input-group mb-3">
        <select 
          class="form-select"
          aria-label="Default select example"
          @change="categorySelected"
          v-model="currentCat"
        >
          <option selected>{{ $t("cat_goods.tip2") }}</option>
          <option 
            v-for="(cat, index) in cat_list"
            :key="index"
            :value="cat"
          >
            {{ cat.name }}
          </option>
        </select>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <button
        class="btn btn-outline-secondary"
        type="button"
        @click="saveGategorizedProducts"
      >
      {{ $t("cat_goods.btn_save") }}
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h4>{{ $t("cat_goods.goods_list") }}</h4>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <!-- {{ $t("cat_goods.filter") }}:  -->
      <input
        type="text"
        class="form-control"
        :placeholder="$t('cat_goods.filter')"
        v-model="filter_name"
        @keyup="filterByName"
      />
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <hr>
    </div>
  </div>
  <div class="list row">
    <div class="col-md-1">
      <input 
          class="form-check-input" 
          type="checkbox" 
          v-model="show_all_categories" 
          id="flexCheckAllCat"
        >
    </div>
    <div class="col-md-11">
      <b>{{ $t("cat_goods.show_other_cat") }}</b>
    </div>
  </div>
  <div class="list row">
    <div class="col-md-1">
      <input 
        class="form-check-input" 
        type="checkbox" 
        v-model="checked_all" 
        id="flexCheckedAll"
        @change="checkedAll"
      >
    </div>
    <div class="col-md-11">
      <b>{{ $t("cat_goods.check_uncheck_all") }}</b>
    </div>
  </div>
  <div
    class="list row"
    v-for="(prod, index) in prod_list"
    :key="index"
  >
    <div class="col-md-1">
      <input 
        class="form-check-input" 
        type="checkbox"
        v-model="prod.checked" 
        id="flexCheckDefault"
      >
    </div>
    <div class="col-md-5">
      {{ prod.name }}
    </div>
    <div class="col-md-4">
      <!-- <span 
        v-for="(cat_name, index) in prod.categories"
        :key="index"
      > {{ cat_name }}, &nbsp;
      </span> -->
    </div>
    <div class="col-md-2">
      <router-link
        :to="'/goods_detail/' + prod.id"
      >Details</router-link>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <hr>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <button
        class="btn btn-outline-secondary"
        type="button"
        @click="saveGategorizedProducts"
      >
      {{ $t("cat_goods.btn_save") }}
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <hr>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  import CategoriesService from "@/services/categories";
  import BillDataService from "@/services/bills";
  import ProductDataService from "@/services/products";
  import { ICategory } from "@/interfaces/categories";
  import { 
    IProduct, ICategorizedProduct, IUncategorizedProduct
  } from "@/interfaces/product";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";

  export default defineComponent({
    name: "cat-prod-list",
    data() {
      return {
        main_header: "" as string,
        currentBillID: "" as string,
        cat_list: [] as ICategory[],
        full_prod_list: [] as IUncategorizedProduct[],
        prod_list: [] as IUncategorizedProduct[],
        currentCat: {} as ICategory,
        list_prod_for_save: [] as IProduct[],
        filter_name : "" as string,
        show_all_categories: false as boolean,
        checked_all: false as boolean
      }
    },
    computed: {
      authToken() {
        const store = useStore();
        console.log("store: ", store);
        return store.state.auth.token;
      },
    },
    methods: {
      async retrieveCategories() {
        try {
          let response = await CategoriesService.getAll(
            this.authToken
          );
          this.cat_list = response.data;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async retrieveBillUncategorizedProducts(
        id: string, cat_id?: string
      ) {
        try {
          let response = await BillDataService.getUncategorizedProducts(
            id, this.authToken, cat_id 
          );
          console.log(
            "retrieveBillUncategorizedProducts result: ",
            response.data
          );
          this.fillProductList(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async retrieveUncategorizedProducts(cat_id?: string) {
        try {
          let response = await ProductDataService.getUncategorized(
            this.authToken, cat_id
          );
          console.log(
            "retrieveUncategorizedProductsresult: ",
            response.data
          );
          this.fillProductList(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      }, 
      async fillProductList(inner_prod_list: IProduct[]){
        this.prod_list = [];
        await this.$nextTick();
        for (let prod of inner_prod_list){
          this.prod_list.push({
            id: prod.id,
            name: prod.name,
            checked: false
          })
        }
        this.full_prod_list = this.prod_list;
        // await this.$nextTick();
        console.log("this.goods_list:", this.prod_list)
      },
      async categorySelected(){
        console.log("categorySelected", this.currentCat);
        try {
          console.log("this.show_all_categories: ", this.show_all_categories);
          if (this.show_all_categories){
            console.log("this.currentCat.id: ", this.currentCat.id);
            await this.getAllProducts(this.currentCat.id);
          } else {
            await this.getAllProducts();
          }
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async saveGategorizedProducts() {
        console.log("saveGategorizedProducts");
        let prod_for_save_list = [] as ICategorizedProduct[];
        for (let prod of this.prod_list) {
          if (prod.checked && this.currentCat) {
            prod_for_save_list.push({
              user_product_id: prod.id,
              cat_id: this.currentCat.id
            })
          }
        }
        console.log(
          "goods_for_save_list: ", prod_for_save_list
        );
        try {
          let response = await ProductDataService.saveCategorized(
            prod_for_save_list, this.authToken
          );
          console.log("saveGategorizedProducts response.data", response.data);
          if (this.show_all_categories){
            await this.getAllProducts(this.currentCat.id);
          } else {
            await this.getAllProducts();
          }
          this.filter_name = "";
          this.checked_all = false;
          this.show_all_categories = false;
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async getAllProducts(cat_id?: string ) {
        console.log("cat_id: ", cat_id);
        if (this.currentBillID) {
          console.log("this.currentBillID: ", this.currentBillID);
          await this.retrieveBillUncategorizedProducts(
            this.currentBillID, cat_id
          );
        } else {
          await this.retrieveUncategorizedProducts(cat_id);
        }
      },
      filterByName() {
        this.prod_list = this.full_prod_list.filter(
          (prod) => { 
            return prod.name.toLowerCase().indexOf(
              this.filter_name.toLowerCase()
            ) != -1
          }
        );
      },
      checkedAll(){
        console.log('checkedAll');
        if (this.checked_all){
          this.prod_list.map((item) => item.checked = true);
        } else {
          this.prod_list.map((item) => item.checked = false);
        }
      }
    },
    async mounted() {

      let bill_id = this.$route.params.bill_id;
      console.log("bill_id: ", bill_id);
      if (typeof bill_id == "string") {
        this.currentBillID = String(bill_id);
      }
      if(this.currentBillID){
        this.main_header = this.$t("cat_goods.head.bill") + ": " + this.currentBillID; 
      } else {
        this.main_header = this.$t("cat_goods.head.all");
      }
      await this.retrieveCategories();
      console.log("this.cat_list.length: ", this.cat_list.length);
      if (!this.cat_list.length){
        this.$router.push({name: "categories"})
      }
      await this.getAllProducts();
    }
})
</script>