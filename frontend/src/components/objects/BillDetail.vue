<template>
    <div class="list row">
      <div class="col-md-8">
      </div>
      <div class="col-md-6">
        <h4>Bill Details</h4>
        <ul class="list-group">
          <li
            class="list-group-item"
            v-for="key in Object.keys(currentBill)"
            :key="key"
          >
            {{ key }}: {{ currentBill[key] }}
          </li>
        </ul>
  
      </div>
    </div>
</template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import BillDataService from "@/services/bills";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import { IBill } from "@/interfaces/bills";
  
  export default defineComponent({
    name: "bill-detail-page",
    data() {
      return {
        currentBillID: "" as string,
        currentBill: {} as IBill
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
      async retrieveBillDetail() {
          if (this.currentBillID) {
            try {
              let response = await BillDataService.get(
                this.currentBillID, this.authToken
              );
              console.log(
                "retrieveBillDetail result:", response.data
              );
              this.currentBill = response.data;
            } catch(e) {
              checkTokenExpired(e);
            }    
          } else {
            alert("empty Goods ID!!");
          }
      }
    },
    async mounted() {
      let bill_id = await this.$route.params.id;
      if (typeof bill_id == "string") {
        console.log("bill_id: ", bill_id);
        console.log("typeof bill_id: ", typeof bill_id);
        this.currentBillID = String(bill_id);
      }
      this.retrieveBillDetail();
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