<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h4>{{ $t("objects.goods.head") }}</h4>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <TableComponent 
          v-if="itemsReady"
          :items="items" 
          :fields="fields"
          :go_to_object="go_to_object"
          :translate_first_column="translate_first_column"
        />
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col">
            <h4>{{ $t("objects.goods.cats") }}</h4>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <ul class="list-group">
              <li
                class="list-group-item"
                v-for="(cat, index) in goods_cat_list"
                :key="index"
              >
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="cat.checked" 
                  id="flexCheckDefault"
                > &nbsp;&nbsp;&nbsp;&nbsp;
                <label 
                  class="form-check-label" 
                  for="flexCheckDefault"
                >
                  {{ cat.name }}
                </label>

              </li>
            </ul>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="updateUserProductCategories"
            >
              {{ $t("objects.goods.btn_save") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import GoodsDataService from "@/services/goods";
  import CategoriesService from "@/services/categories";
  import ProductDataService from "@/services/products";
  import { IGoods, IUncategorizedGoods } from "@/interfaces/goods";
  import { ICategory } from "@/interfaces/categories";
  import { IUserProductCategories } from "@/interfaces/user_products";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import TableComponent from '@/components/utils/TableComponent.vue';
  
  export default defineComponent({
    name: "goods-detail-page",
    components: { TableComponent },
    data() {
      return {
        currentGoodsID: "" as string,
        currentGoods: {} as IGoods,
        full_cat_list: [] as ICategory[],
        goods_cat_list: [] as IUncategorizedGoods[],
        itemsReady: false as boolean,
        translate_first_column: true as boolean,
        go_to_object: "bills" as string,
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
      async retrieveCategories() {
          try {
              let response = await CategoriesService.getAll(
                  this.authToken
              );
              this.full_cat_list = response.data;
              console.log(response.data);
          } catch(e) {
              checkTokenExpired(e);
          }
      },
      async retrieveGoodsDetail() {
          if (this.currentGoodsID) {
            try {
              let response = await GoodsDataService.get(
                this.currentGoodsID, this.authToken
              );
              console.log(
                "retrieveGoodsDetail result:", response.data
              );
              this.currentGoods = response.data;
              this.prepareTableItems();
              this.prepareListCategories();
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
        for (let key of Object.keys(this.currentGoods)){
          if (
            key == "id" 
            || key == "seller_id" 
            || key == "user_id" 
            || key == "image"
            || key == "bill_id"
            || key == "unit_id"
            || key == "categories"
            || key == "user_product"
          ){
            continue;
          }
          let value_obj = Object(this.currentGoods)[String(key)];
          let value = value_obj;
          if (key == "seller"){
            value = "";
            value += value_obj.official_name + ", ";
            value += value_obj.address;
          } else if (key == "unit") {
            value = value_obj.name;
          }
          items.push({
              "Field": key,
              "Value": value,
            })
        }
        this.items = items;
        this.itemsReady = true;
      },
      async updateUserProductCategories() {
        console.log("saveGoodsGategories");
        let data_for_update = {
          user_product_id: this.currentGoods.user_product.id,
          list_cat_id: [] as String[]
        } as IUserProductCategories;
        console.log(
          "this.currentGoods.user_product.id: ",
          this.currentGoods.user_product.id
        )
        for (let cat of this.goods_cat_list) {
          if (cat.checked) {
            data_for_update.list_cat_id.push(cat.id);
          }
        }
        console.log("data_for_update: ", data_for_update);
        try {
          let response = await ProductDataService.updateCategory(
            data_for_update, this.authToken
          );
          console.log(
            "saveGategorizedGoods response.data",
            response.data
          );
          if (!response.data){
            alert("Server error!!");
            return;
          }
          this.retrieveGoodsDetail();
          this.prepareListCategories();
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      prepareListCategories() {
        this.goods_cat_list = [];
        for (let cat of this.full_cat_list) {
            let checked_cat = false;
            let current_cat_ids = []; 
            for (let good_cat of this.currentGoods.user_product.categories){
              current_cat_ids.push(good_cat.id);
            }
            console.log("current_cat_ids: ", current_cat_ids);
            console.log("cat.id: ", cat.id);
            if (current_cat_ids.includes(cat.id)) {
              checked_cat = true;
              console.log("checked_cat: ", checked_cat);
            }
            this.goods_cat_list.push({
                id: cat.id,
                name: cat.name,
                checked: checked_cat,
                categories: []
            })
        }
      }
    },
    async mounted() {
      let goods_id = await this.$route.params.id;
      if (typeof goods_id == "string") {
        console.log("goods_id: ", goods_id);
        console.log("typeof goods_id: ", typeof goods_id);
        this.currentGoodsID = String(goods_id);
      }
      this.retrieveCategories();
      this.retrieveGoodsDetail();
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