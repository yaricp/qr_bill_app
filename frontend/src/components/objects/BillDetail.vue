<template>
    <div class="list row">
      <div class="col">
        <h4>Bill Details</h4>
      </div>
      <div class="col">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="goToCategorizing()"
        > 
        Categorize goods
        </button>
      </div>
    </div>
    <div class="list row">
      <div class="col">
        <TableComponent 
          v-if="itemsReady"
          :data="items" 
          :fields="fields"
          :go_to_object="go_to_object"
        />
      </div>
    </div>
    <div class="list row">
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
  import TableComponent from '@/components/utils/TableComponent.vue';
  
  export default defineComponent({
    name: "bill-detail-page",
    components: { TableComponent },
    data() {
      return {
        currentBillID: "" as string,
        currentBill: {} as IBill,
        itemsReady: false as boolean,
        go_to_object: "category_goods_bill_id" as string,
        fields: [
          "Field", "Value"
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
              this.prepareTableItems();
            } catch(e) {
              checkTokenExpired(e);
            }    
          } else {
            alert("empty Goods ID!!");
          }
      },
      prepareTableItems(){
        this.itemsReady = false;
        let items = [];
        for (let key of Object.keys(this.currentBill)){
          if (key == "id" || key == "seller_id" || key == "user_id" || key == "image"){
            continue;
          }
          let value_obj = Object(this.currentBill)[String(key)];
          let value = value_obj;
          if (key == "goods_list"){
            value = "";
            for (let item of value_obj){
              value += item.name + ", ";
            }
          } else if (key == "seller"){
            value = "";
            value += value_obj.official_name + ", ";
            value += value_obj.address;
          }
          items.push({
              "Field": key,
              "Value": value,
            })
        }
        this.items = items;
        this.itemsReady = true;
      },
      goToCategorizing(){
        this.$router.push({
          name: String(this.go_to_object),
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