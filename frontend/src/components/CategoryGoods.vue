<template>
  <div class="row">
    <div class="col-md-12">
      <h3>{{ main_header }}</h3>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <div class="input-group mb-3">
        <p>Choose category for items below</p>
      </div>
      <div class="input-group mb-3">
        <select 
          class="form-select"
          aria-label="Default select example"
          @change="categorySelected"
          v-model="currentCat"
        >
          <option selected>Open this select menu</option>
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
        @click="saveGategorizedGoods"
      >
        Save category for selected items
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h4>Goods List</h4>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      Filter: 
      <input
        type="text"
        class="form-control"
        placeholder="Filter by name"
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
  <div class="row">
    <div class="col-md-1">
      <input 
        class="form-check-input" 
        type="checkbox" 
        v-model="show_all_categories" 
        id="flexCheckAllCat"
      >
    </div>
    <div class="col-md-11">
      <b> Show with other categories</b>
    </div>
  </div>
  <div class="row">
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
      <b>Check/Uncheck All</b>
    </div>
  </div>
  <div
    class="row"
    v-for="(goods, index) in goods_list"
    :key="index"
  >
    <div class="col-md-1">
      <input 
        class="form-check-input" 
        type="checkbox"
        v-model="goods.checked" 
        id="flexCheckDefault"
      >
    </div>
    <div class="col-md-5">
      {{ goods.name }}
    </div>
    <div class="col-md-4">
      <span 
        v-for="(cat_name, index) in goods.categories"
        :key="index"
      > {{ cat_name }}, &nbsp;
      </span>
    </div>
    <div class="col-md-2">
      <router-link
        :to="'/goods_detail/' + goods.id"
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
        @click="saveGategorizedGoods"
      >
        Save category for selected items
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
  import GoodsDataService from "@/services/goods";
  import { ICategory } from "@/interfaces/categories";
  import { ICategorizedGoods } from "@/interfaces/goods";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import { IGoods, IUncategorizedGoods } from "@/interfaces/goods";

  export default defineComponent({
    name: "categories-list",
    compatConfig: { MODE: 3 },
    data() {
      return {
        main_header: "" as string,
        currentBillID: "" as string,
        cat_list: [] as ICategory[],
        full_goods_list: [] as IUncategorizedGoods[],
        goods_list: [] as IUncategorizedGoods[],
        currentCat: {} as ICategory,
        list_goods_for_save: [] as IGoods[],
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
      async retrieveBillUncategorizedGoods(
        id: string, cat_id?: string
      ) {
        try {
          let response = await BillDataService.getUncategorizedGoods(
            id, this.authToken, cat_id 
          );
          console.log(
            "retrieveBillUncategorizedGoods result: ",
            response.data
          );
          this.fillGoodsList(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async retrieveUncategorizedGoods(cat_id?: string) {
        try {
          let response = await GoodsDataService.getUncategorized(
            this.authToken, cat_id
          );
          console.log(
            "retrieveUncategorizedGoodsresult: ",
            response.data
          );
          this.fillGoodsList(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      }, 
      async fillGoodsList(goods_list: IGoods[]){
        this.goods_list = [];
        await this.$nextTick();
        for (let goods of goods_list){
          let list_cat_names: string[] = goods.categories.map(
            (item) => item.name
          );
            this.goods_list.push({
                id: goods.id,
                name: goods.name,
                checked: false,
                categories: list_cat_names
            })
        }
        this.full_goods_list = this.goods_list;
        // await this.$nextTick();
        console.log("this.goods_list:", this.goods_list)
      },
      async categorySelected(){
        console.log("categorySelected", this.currentCat);
        try {
          console.log("this.show_all_categories: ", this.show_all_categories);
          if (this.show_all_categories){
            await this.getAllGoods(this.currentCat.id);
          } else {
            await this.getAllGoods();
          }
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async saveGategorizedGoods() {
        console.log("saveGategorizedGoods");
        let goods_for_save_list = [] as ICategorizedGoods[];
        for (let goods of this.goods_list) {
          if (goods.checked && this.currentCat) {
            goods_for_save_list.push({
              goods_id: goods.id,
              cat_id: this.currentCat.id
            })
          }
        }
        console.log(
          "goods_for_save_list: ", goods_for_save_list
        );
        try {
          let response = await GoodsDataService.saveCategorized(
            goods_for_save_list, this.authToken
          );
          console.log("saveGategorizedGoods response.data", response.data);
          if (this.show_all_categories){
            await this.getAllGoods(this.currentCat.id);
          } else {
            await this.getAllGoods();
          }
          this.filter_name = "";
          this.checked_all = false;
          this.show_all_categories = false;
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async getAllGoods(cat_id?: string ) {
        console.log("cat_id: ", cat_id);
        if (this.currentBillID) {
          console.log("this.currentBillID: ", this.currentBillID);
          await this.retrieveBillUncategorizedGoods(
            this.currentBillID, cat_id
          );
        } else {
          await this.retrieveUncategorizedGoods(cat_id);
        }
      },
      filterByName() {
        this.goods_list = this.full_goods_list.filter(
          (item) => { 
            return item.name.toLowerCase().indexOf(
              this.filter_name.toLowerCase()
            ) != -1
          }
        );

        // this.inner_data = this.$props.data.filter(
        //         (item: any) => {return (
        //             item.name.toLowerCase().indexOf(
        //                 this.search_name.toLowerCase()
        //             ) != -1
        //         )}
        //     )

      },
      checkedAll(){
        console.log('checkedAll');
        if (this.checked_all){
          this.goods_list.map((item) => item.checked = true);
        } else {
          this.goods_list.map((item) => item.checked = false);
        }
      }
    },
    async mounted() {

      let bill_id = this.$route.params.bill_id;
      if (typeof bill_id == "string") {
        this.currentBillID = String(bill_id);
      }
      if(this.currentBillID){
        this.main_header = "Uncategorized items for bill with ID: " + this.currentBillID; 
      } else {
        this.main_header = "All your uncategorized items";
      }
      await this.retrieveCategories();
      if (!this.cat_list.length){
        this.$router.push({name: "categories"})
      }
      await this.getAllGoods();
    }
})
</script>