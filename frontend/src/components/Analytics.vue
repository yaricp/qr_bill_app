<template>
    <div>
      <h4>Analitics</h4>

    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import GoodsDataService from "@/services/goods";
import Goods from "@/interfaces/goods";
import ResponseData from "@/interfaces/ResponseData";

export default defineComponent({
  name: "analitics-page",
  data() {
    return {
      goods_list: [] as Goods[],
      message: "",
    };
  },
  methods: {
    async retrieveGoods() {
      try {
        let response = await GoodsDataService.getAll();
        this.goods_list = response.data;
        console.log(response.data);
      } catch(e) {
        console.log(e);
      }
    },
  },
  mounted() {
      this.retrieveGoods();
    },
});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>