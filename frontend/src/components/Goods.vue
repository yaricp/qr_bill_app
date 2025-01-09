<template>
    <div class="list row">
      <div class="col-md-8">
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Filter by name"
            v-model="filter_name"
          />
          <div class="input-group-append">
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="filterByName"
            >
              Search
            </button>
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
        <div v-else>
          <br />
          <p>Please click on a Goods...</p>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import axios, {AxiosError} from "axios";
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import { IGoods } from "@/interfaces/goods";
  import ResponseData from "@/interfaces/ResponseData";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  
  export default defineComponent({
    name: "goods-list",
    data() {
      return {
        goods_list: [] as IGoods[],
        currentGoods: {} as IGoods,
        currentIndex: -1,
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
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      refreshList() {
        this.retrieveGoods();
        this.currentGoods = {} as IGoods;
        this.currentIndex = -1;
      },
      setActiveGoods(tutorial: IGoods, index = -1) {
        this.currentGoods = tutorial;
        this.currentIndex = index;
      },
      filterByName() {
        this.goods_list = this.goods_list.filter(
          (item) => { item.name == this.filter_name}
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