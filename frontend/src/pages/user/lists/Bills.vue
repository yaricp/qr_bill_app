<template>
  <div class="row">
    <div class="col"> 
    </div>
    <div class="col">     
    </div>
    <div class="col">
      <button
        class="btn btn-outline-secondary"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#staticBackdrop"
        @click="new_bill_showed =!new_bill_showed"
      >
        {{ $t("lists.bills.new.open_new_bill_btn_text") }}
      </button>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <h4>{{ $t("lists.bills.head") }}</h4>
      <TableComponent 
        v-if="itemsReady"
        :items="items" 
        :fields="fields"
        :go_to_object="go_to_object"
        :field_search="field_search"
        :show_paginator="true"
      />
    </div>
  </div>

  <div 
    class="modal fade" 
    id="staticBackdrop"
    data-bs-backdrop="static"
    data-bs-keyboard="false"
    tabindex="-1"
    aria-labelledby="staticBackdropLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">
            {{ $t("lists.bills.new.header")}}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close">
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">{{ $t("lists.bills.new.seller") }}</div>
            <div class="col">
              <input type="text" v-model="new_seller"/>
            </div>
          </div>
          <div class="row">
            <div class="col">{{ $t("lists.bills.new.product") }}</div>
            <div class="col">
              <input type="text" v-model="new_product"/>
            </div>
          </div>
          <div class="row">
            <div class="col">{{ $t("lists.bills.new.sum") }}</div>
            <div class="col">
              <input type="text" v-model="new_sum"/>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button 
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            {{ $t("lists.bills.new.cancel_btn_text")}}
          </button>
          <button 
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="saveNewBill"
          >
          {{ $t("lists.bills.new.save_btn_text")}}
          </button>
        </div>
      </div>
    </div>
  </div>

</template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import BillsDataService from "@/services/bills";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import { IBill } from "@/interfaces/bills";
  import TableComponent from '@/components/utils/TableComponent.vue';
  
  export default defineComponent({
    name: "bills-list",
    components: { TableComponent },
    data() {
      return {
        bills_list: [] as IBill[],
        itemsReady: false as boolean,
        new_bill_showed : false as boolean,
        go_to_object: "bill_detail" as string,
        field_search: "Seller" as string,
        fields: [
          "Created", "Seller", "Summ", "Image", "ID"
        ],
        new_seller: "" as string,
        new_product: "" as string,
        new_sum: "" as string,
        items: [] as Array<Object>
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
      async retrieveBills(offset: number, limit: number) {
        try {
          let response = await BillsDataService.getAll(
            offset=offset, limit=limit, this.authToken
          );
          if (response.data){
            return response.data;
          } else {
            return [];
          }
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      prepareTableItems(){
        this.itemsReady = false;
        let items = [];
        for (let bill of this.bills_list){
          items.push({
            "Created": new Date(bill.created).toLocaleString(
              this.$t("short_lang")
            ),
            "Seller": bill.seller.official_name,
            "Summ": Number(bill.value),
            "Image": bill.image ? bill.id : "",
            "ID": bill.id
          })
        }
        this.items = items;
        // console.log(this.items);
        this.itemsReady = true;
      },
      async saveNewBill() {
        console.log("saveNewBill");
        let new_bill_data = {
          "seller": this.new_seller,
          "product": this.new_product,
          "sum": this.new_sum
        }
        console.log("new_bill_data: ", new_bill_data);
        try {
          let response = await BillsDataService.create(
            new_bill_data, this.authToken
          );
          console.log("response: ", response);
          if (response.status == 200) {
            this.bills_list.push(response.data);
            this.prepareTableItems();
          } else {
            console.log("response.data: ", response.data)
          }
        } catch(err) {
          console.log("Error: ", err);
        }
      }
    },
    async mounted() {
      let first_result = await this.retrieveBills(0, 10);
      this.bills_list = first_result;
      this.prepareTableItems();
      let next_result = await this.retrieveBills(10, 0);
      this.bills_list = [...this.bills_list, ...next_result];
      this.prepareTableItems();
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