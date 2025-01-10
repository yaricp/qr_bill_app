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
        </div>
      </div>
      <div class="col-md-6">
        <h4>Goods List</h4>
        <ul class="list-group">
          <li
            class="list-group-item"
            v-for="(goods, index) in goods_list"
            :key="index"
            @click="goToGoods(goods)"
          >
            {{ goods.name }}
          </li>
        </ul>
  
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import { IGoods } from "@/interfaces/goods";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  
  export default defineComponent({
    name: "goods-list",
    data() {
      return {
        goods_list: [] as IGoods[],
        full_goods_list: [] as IGoods[],
        filter_name: "",
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
      async retrieveGoods() {
        try {
          let response = await GoodsDataService.getAll(
            this.authToken
          );
          this.goods_list = response.data;
          this.full_goods_list = this.goods_list;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      goToGoods(goods: IGoods) {
        this.$router.push({
          name: "goods_detail", params: { goods_id: goods.id}
        });
      },
      filterByName() {
        this.goods_list = this.full_goods_list.filter(
          (item) => { return item.name.includes(this.filter_name)}
        );
      },
    },
    mounted() {
      this.retrieveGoods();
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