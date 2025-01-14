<template>
    <div class="list row">
      <div class="col-md-6">
        <h4>Bills List</h4>
        <TableComponent 
          v-if="itemsReady"
          :data="items" 
          :fields="fields"
          :go_to_object="go_to_object"
          :field_search="field_search"
        />
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
        full_bills_list: [] as IBill[],
        filter_created: "",
        itemsReady: false as boolean,
        go_to_object: "bill_detail" as string,
        field_search: "Seller" as string,
        fields: [
          "Created", "Seller", "Summ", "Image", "ID"
        ],
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
      async retrieveBills() {
        try {
          let response = await BillsDataService.getAll(
            this.authToken
          );
          this.bills_list = response.data;
          this.full_bills_list = this.bills_list;
          this.prepareTableItems();
          // console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      prepareTableItems(){
        this.itemsReady = false;
        let items = [];
        for (let bill of this.bills_list){
          items.push({
            "Created": bill.created,
            "Seller": bill.seller.official_name,
            "Summ": Number(bill.value),
            "Image": bill.image,
            "ID": bill.id
          })
        }
        this.items = items;
        // console.log(this.items);
        this.itemsReady = true;
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
        this.prepareTableItems();
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