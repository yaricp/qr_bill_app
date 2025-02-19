<template>
    <div class="row">
      <div class="col">
        <h4>
            {{ $t("objects.bill.photo.header") }}: &nbsp;
            {{ currentBill.id }}
        </h4>
      </div>
    </div>
    <div class="row">
        <div class="col">
          <hr>
        </div>
      </div>
    <div class="row">
      <div class="col">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="goToBill()"
        > 
        {{ $t("objects.bill.photo.btn_goto_bill") }}
        </button>
      </div>
    </div>
    <div class="row">
        <div class="col">
          <hr>
        </div>
      </div>
    <div class="row">
      <div class="col">
        <img :src="currentBill.image">
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
    name: "bill-photo-page",
    data() {
      return {
        currentBillID: "" as string,
        currentBill: {} as IBill,
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
      },
      goToBill(){
        this.$router.push({
          name: "bill_detail",
          params: {bill_id: this.currentBill.id}
        });
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