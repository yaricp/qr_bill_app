<template>
    <div class="list row">
      <div class="col-md-6">
        <h4>Goods List</h4>
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
  import GoodsDataService from "@/services/goods";
  import { IGoods } from "@/interfaces/goods";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import TableComponent from '@/components/utils/TableComponent.vue';
  
  export default defineComponent({
    name: "goods-list",
    components: { TableComponent },
    data() {
      return {
        goods_list: [] as IGoods[],
        full_goods_list: [] as IGoods[],
        filter_name: "",
        itemsReady: false as boolean,
        go_to_object: "goods_detail" as string,
        field_search: "Name" as string,
        fields: [
          "Name", "Price", "Unit", "Quantity", "Summ", "Seller", "ID"
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
      async retrieveGoods() {
        try {
          let response = await GoodsDataService.getAll(
            this.authToken
          );
          this.goods_list = response.data;
          this.full_goods_list = this.goods_list;
          await this.prepareTableItems();
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async prepareTableItems(){
        console.log("prepareTableItems");
        this.itemsReady = false;
        let items = [];
        for (let goods of this.goods_list){
          items.push({
            "Name": goods.name,
            "Price": Number(goods.unit_price_after_vat),
            "Unit": goods.unit.name,
            "Quantity": Number(goods.quantity),
            "Summ": Number(goods.price_after_vat),
            "Seller": goods.seller.official_name,
            "ID": goods.id
          })
        }
        this.items = items;
        this.itemsReady = true;
        await this.$nextTick();
      },
      async filterByName() {
        this.goods_list = this.full_goods_list.filter(
          (item) => { return item.name.includes(this.filter_name)}
        );
        console.log("this.goods_list: ", this.goods_list)
        await this.prepareTableItems();
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