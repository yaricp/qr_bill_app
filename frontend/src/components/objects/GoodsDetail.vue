<template>
    <div class="list row">
      <div class="col-md-8">
      </div>
      <div class="col-md-6">
        <h4>Goods Details</h4>
        <ul class="list-group">
          <li
            class="list-group-item"
            v-for="key in Object.keys(currentGoods)"
            :key="key"
          >
            {{ key }}: {{ currentGoods[key] }}
          </li>
        </ul>
  
      </div>
      <div class="col-md-6">
        <h4>Categories</h4>
          <div>
            <ul class="list-group">
              <li
                class="list-group-item"
                v-for="(cat, index) in goods_cat_list"
                :key="index"
              >
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="cat.checked" 
                  id="flexCheckDefault"
                > &nbsp;&nbsp;&nbsp;&nbsp;
                <label 
                  class="form-check-label" 
                  for="flexCheckDefault"
                >
                  {{ cat.name }} - {{ cat.checked }}
                </label>

              </li>
            </ul>
          </div>
          <div class="col-md-12">
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="saveGoodsGategories"
          >
            Save
          </button>
    </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import CategoriesService from "@/services/categories";
  import { IGoods, IUncategorizedGoods, ICategorizedGoods } from "@/interfaces/goods";
  import { ICategory } from "@/interfaces/categories";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  
  export default defineComponent({
    name: "goods-detail-page",
    data() {
      return {
        currentGoodsID: "" as string,
        currentGoods: {} as IGoods,
        full_cat_list: [] as ICategory[],
        goods_cat_list: [] as IUncategorizedGoods[]
      };
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
              this.full_cat_list = response.data;
              console.log(response.data);
          } catch(e) {
              checkTokenExpired(e);
          }
      },
      async retrieveGoodsDetail() {
          if (this.currentGoodsID) {
            try {
              let response = await GoodsDataService.get(
                this.currentGoodsID, this.authToken
              );
              console.log(
                "retrieveGoodsDetail result:", response.data
              );
              this.currentGoods = response.data;
              this.prepareListCategories();
            } catch(e) {
              checkTokenExpired(e);
            }    
          } else {
            alert("empty Goods ID!!");
          }
      },
      async saveGoodsGategories() {
          console.log("saveGoodsGategories");
          let goods_for_save_list = [] as ICategorizedGoods[];
          for (let cat of this.goods_cat_list) {
              if (cat.checked) {
                  goods_for_save_list.push({
                      goods_id: this.currentGoods.id,
                      cat_id: cat.id
                  })
              }
          }
          console.log(
              "goods_for_save_list: ", goods_for_save_list
          );
          console.log("typeof this.currentGoodsID:", typeof this.currentGoodsID);
          try {
              let response = await GoodsDataService.updateCategory(
                this.currentGoodsID, goods_for_save_list, this.authToken
              );
              console.log("saveGategorizedGoods response.data", response.data);
              if (!response.data){
                alert("Server error!!");
                return;
              }
              this.retrieveGoodsDetail();
              this.prepareListCategories();
          } catch(e) {
              checkTokenExpired(e);
          }
      },
      prepareListCategories() {
        this.goods_cat_list = [];
        for (let cat of this.full_cat_list) {
            let checked_cat = false;
            let current_cat_ids = []; 
            for (let good_cat of this.currentGoods.categories){
              current_cat_ids.push(good_cat.id);
            }
            console.log("current_cat_ids: ", current_cat_ids);
            console.log("cat.id: ", cat.id);
            if (current_cat_ids.includes(cat.id)) {
              checked_cat = true;
              console.log("checked_cat: ", checked_cat);
            }
            this.goods_cat_list.push({
                id: cat.id,
                name: cat.name,
                checked: checked_cat,
                categories: []
            })
        }
      }
    },
    async mounted() {
      let goods_id = await this.$route.params.goods_id;
      if (typeof goods_id == "string") {
        console.log("goods_id: ", goods_id);
        console.log("typeof goods_id: ", typeof goods_id);
        this.currentGoodsID = String(goods_id);
      }
      this.retrieveCategories();
      this.retrieveGoodsDetail();
    },
  });
  </script>
  
  <style>
  .list {
    text-align: left;
    max-width: 750px;
    margin: auto;
  }
  </style>