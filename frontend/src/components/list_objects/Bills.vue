<template>
    <div class="list row">
      <div class="col-md-8">
        <div class="input-group mb-3">
          Filter by date: <input
            type="text"
            class="form-control"
            placeholder="Filter by name"
            v-model="filter_created"
            @keyup="filterByCreated"
          />
        </div>
      </div>
      <div class="col-md-6">
        <h4>Bills List</h4>
        <ul class="list-group">
          <li
            class="list-group-item"
            v-for="(bill, index) in bills_list"
            :key="index"
            @click="goToBill(bill)"
          >
            <p>
                {{ bill.created }} - 
                {{ bill.value }} 
                <img :src="bill.image"/>
            </p>
          </li>
        </ul>
  
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import BillsDataService from "@/services/bills";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import { IBill } from "@/interfaces/bills";
  
  export default defineComponent({
    name: "bills-list",
    data() {
      return {
        bills_list: [] as IBill[],
        full_bills_list: [] as IBill[],
        filter_created: "",
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
      async retrieveBills() {
        try {
          let response = await BillsDataService.getAll(
            this.authToken
          );
          this.bills_list = response.data;
          this.full_bills_list = this.bills_list;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      goToBill(bill: IBill) {
        // this.$router.push({
        //   name: "bills_detail", params: { bill_id: bill.id}
        // });
      },
      filterByCreated() {
        this.bills_list = this.full_bills_list.filter(
          (item) => { return item.created.includes(this.filter_created)}
        );
      },
    },
    mounted() {
      this.retrieveBills();
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