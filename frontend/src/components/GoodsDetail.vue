<template>
    <div class="list row">
      <div class="col-md-8">
        <div class="input-group mb-3">
          Filter: <input
            type="text"
            class="form-control"
            placeholder="Filter by name"
            v-model="filter_name"
            @keyup="filterByName"
          />
          <div class="input-group-append">
            <!-- <button
              class="btn btn-outline-secondary"
              type="button"
              @click="filterByName"
            >
              Search
            </button> -->
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <h4>Goods List</h4>
        <ul class="list-group">
          <li
            class="list-group-item"
            :class="{ active: index == currentIndex }"
            v-for="(goods, index) in goods_list"
            :key="index"
            @click="setActiveGoods(goods, index)"
          >
            {{ goods.name }}
          </li>
        </ul>
  
      </div>
      <div class="col-md-6">
        <div v-if="currentGoods.id">
          <h4>Tutorial</h4>
          <div>
            <label><strong>Name:</strong></label> {{ currentGoods.title }}
          </div>
  
          <router-link
            :to="'/goods/' + currentGoods.id"
            class="badge badge-warning"
            >Edit</router-link
          >
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
            let goods_id = this.$route.params.goods_id;
            if (typeof goods_id == "string") {
                console.log("goods_id: ", goods_id);
                try {
                    let response = await GoodsDataService.get(
                        goods_id, this.authToken
                    );
                    console.log(
                        "retrieveGoodsDetail result:", response.data
                    );
                    this.currentGoods = response.data;
                    this.prepareListCategories();
                } catch(e) {
                    checkTokenExpired(e);
                }    
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
            try {
                let response = await GoodsDataService.saveCategorized(
                    goods_for_save_list, this.authToken
                );
                console.log("saveGategorizedGoods response.data", response.data);
                this.currentGoods = response.data;
            } catch(e) {
                checkTokenExpired(e);
            }
        },
        prepareListCategories() {
            this.goods_cat_list = [];
            for (let cat of this.full_cat_list) {
                let checked_cat = false;
                if (this.currentGoods.categories.includes(cat)) {
                    checked_cat = true;
                }
                this.goods_cat_list.push({
                    id: cat.id,
                    name: cat.name,
                    checked: checked_cat
                })
            }
        }
    },
    mounted() {
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