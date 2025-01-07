<template>
    <div class="submit-form">
      <div v-if="!submitted">
        <div class="form-group">
          <label for="title">Title</label>
          <input
            type="text"
            class="form-control"
            id="name"
            required
            v-model="goods.name"
            name="name"
          />
        </div>
  
        <button @click="saveGoods" class="btn btn-success">Submit</button>
      </div>
  
      <div v-else>
        <h4>You submitted successfully!</h4>
        <button class="btn btn-success" @click="newGoods">Add</button>
      </div>
    </div>
  </template>
  
<script lang="ts">
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import { IGoods } from "@/interfaces/goods";
  import ResponseData from "@/interfaces/ResponseData";
  import { useStore } from '@/store';
  
  export default defineComponent({
    name: "add-goods",
    data() {
      return {
        goods: {
          id: null,
          name: ""
        } as IGoods,
        submitted: false,
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
      saveGoods() {
        let data = {
          name: this.goods.name
        };
  
        GoodsDataService.create(data,this.authToken)
          .then((response: ResponseData) => {
            this.goods.id = response.data.id;
            console.log(response.data);
            this.submitted = true;
          })
          .catch((e: Error) => {
            console.log(e);
          });
      },
      newGoods() {
        this.submitted = false;
        this.goods = {} as IGoods;
      },
    },
  });
</script>
  
  <style>
  .submit-form {
    max-width: 300px;
    margin: auto;
  }
  </style>