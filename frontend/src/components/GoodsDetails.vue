<template>
    <div v-if="currentGoods.id" class="edit-form">
      <h4>Goods</h4>
      <form>
        <div class="form-group">
          <label for="title">Name</label>
          <input
            type="text"
            class="form-control"
            id="name"
            v-model="currentGoods.name"
          />
        </div>
        <div class="form-group">
          <label for="price_after_vat">Price After Vat</label>
          <input
            type="text"
            class="form-control"
            id="price_after_vat"
            v-model="currentGoods.price_after_vat"
          />
        </div>
        <div class="form-group">
          <label><strong>Rebate Reducing:</strong></label>
          {{ currentGoods.rebate_reducing ? "True" : "False" }}
        </div>
      </form>
  
      <button class="badge badge-danger mr-2" @click="deleteGoods">
        Delete
      </button>
  
      <button type="submit" class="badge badge-success" @click="updateGoods">
        Update
      </button>
      <p>{{ message }}</p>
    </div>
  
    <div v-else>
      <br />
      <p>Please click on a Goods...</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import { IGoods } from "@/interfaces/goods";
  import ResponseData from "@/interfaces/ResponseData";
  
  export default defineComponent({
    name: "goods-detail",
    data() {
      return {
        currentGoods: {} as IGoods,
        message: "",
      };
    },
    methods: {
      getGoods(id: any) {
        GoodsDataService.get(id)
          .then((response: ResponseData) => {
            this.currentGoods = response.data;
            console.log(response.data);
          })
          .catch((e: Error) => {
            console.log(e);
          });
      },
  
      updateGoods() {
        GoodsDataService.update(this.currentGoods.id, this.currentGoods)
          .then((response: ResponseData) => {
            console.log(response.data);
            this.message = "The tutorial was updated successfully!";
          })
          .catch((e: Error) => {
            console.log(e);
          });
      },
  
      deleteGoods() {
        GoodsDataService.delete(this.currentGoods.id)
          .then((response: ResponseData) => {
            console.log(response.data);
            this.$router.push({ name: "tutorials" });
          })
          .catch((e: Error) => {
            console.log(e);
          });
      },
    },
    mounted() {
      this.message = "";
      this.getGoods(this.$route.params.id);
    },
  });
  </script>
  
  <style>
  .edit-form {
    max-width: 300px;
    margin: auto;
  }
  </style>