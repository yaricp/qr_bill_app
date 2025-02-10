<template>
    <div class="row">
      <div class="col">
        <h4>{{ $t("lists.goods.head") }}</h4>
        <TableComponent 
          v-if="itemsReady"
          :items="items" 
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
      async retrieveGoods(offset: number, limit: number) {
        try {
          let response = await GoodsDataService.getAll(
            offset, limit, this.authToken
          );
          console.log("response.data: ", response.data);
          if (response.data){
            return response.data;
          } else {
            return [];
          }
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
        console.log("After nextTick");
      }
    },
    async mounted() {
      let result = await this.retrieveGoods(0, 10);
      this.goods_list = result;
      await this.prepareTableItems();
      let next_result = await this.retrieveGoods(10, 0);
      this.goods_list = [...this.goods_list, ...next_result];
      await this.prepareTableItems();
      console.log("after all preparing");
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