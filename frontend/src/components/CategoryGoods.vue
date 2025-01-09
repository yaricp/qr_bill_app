<template>
    <div class="list row">
    <div class="col-md-12">
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
    <div class="col-md-12">
      <button
        class="btn btn-outline-secondary"
        type="button"
        @click="saveGategorizedGoods"
      >
        Save
      </button>
    </div>
    <div class="col-md-12">
      <h4>Goods List</h4>
      Filter: <input
            type="text"
            class="form-control"
            placeholder="Filter by name"
            v-model="filter_name"
            @keyup="filterByName"
          />
      <ul class="list-group">
        <li
          class="list-group-item"
          v-for="(goods, index) in goods_list"
          :key="index"
        >
          <input 
            class="form-check-input" 
            type="checkbox" 
            :value="goods.checked" 
            id="flexCheckDefault"
            @change="goodsChecked(index)"
          > &nbsp;&nbsp;&nbsp;&nbsp;
          <label 
            class="form-check-label" 
            for="flexCheckDefault"
          >
            {{ goods.name }}
          </label> 
        </li>
      </ul>
    </div>
    <div class="col-md-12">
      <button
        class="btn btn-outline-secondary"
        type="button"
        @click="saveGategorizedGoods"
      >
        Save
      </button>
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
        cat_list: [] as ICategory[],
        full_goods_list: [] as IUncategorizedGoods[],
        goods_list: [] as IUncategorizedGoods[],
        currentCat: {} as ICategory,
        list_goods_for_save: [] as IGoods[],
        filter_name : "" as string
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
          this. cat_list = response.data;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async retrieveBillUncategorizedGoods(
        cat_id: string, id: string
      ) {
        try {
          let response = await BillDataService.getUncategorizedGoods(
            id, cat_id, this.authToken
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
      async retrieveUncategorizedGoods(cat_id: string) {
        try {
          let response = await GoodsDataService.getUncategorized(
            cat_id, this.authToken
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
            this.goods_list.push({
                id: goods.id,
                name: goods.name,
                checked: false
            })
        }
        this.full_goods_list = this.goods_list;
        await this.$nextTick();
        console.log("this.goods_list:", this.goods_list)
      },
      async categorySelected(){
        console.log("categorySelected", this.currentCat);
        try {
          await this.getAllGoods(this.currentCat.id);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      goodsChecked(index: number) {
        if (this.goods_list[index].checked){
          this.goods_list[index].checked = false;
        } else {
          this.goods_list[index].checked = true;
        }
        console.log("this.goods_list: ", this.goods_list);
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
          await this.getAllGoods(this.currentCat.id);
          this.filter_name = "";
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async getAllGoods(cat_id: string) {
        console.log("cat_id: ", cat_id);
        console.log(
          "this.$route.params: ", this.$route.params
        );

        let bill_id = this.$route.params.bill_id;
        console.log("typeof bill_id: ", typeof bill_id)
        if (typeof bill_id == "string") {
          console.log("bill_id: ", bill_id);
          await this.retrieveBillUncategorizedGoods(cat_id, bill_id);
        } else {
          await this.retrieveUncategorizedGoods(cat_id);
        }
      },
      filterByName() {
        this.goods_list = this.full_goods_list.filter(
          (item) => { return item.name.includes(this.filter_name)}
        );
      }
    },
    async mounted() {
        await this.retrieveCategories();
        // await this.getAllGoods();
    }
})
</script>