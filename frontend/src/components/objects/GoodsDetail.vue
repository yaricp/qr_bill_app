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
          :data="items" 
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
                  {{ cat.name }} - {{ cat.checked }}
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
              @click="saveGoodsGategories"
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
  import { IGoods, IUncategorizedGoods, ICategorizedGoods } from "@/interfaces/goods";
  import { ICategory } from "@/interfaces/categories";
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
      async saveGoodsGategories() {
          console.log("saveGoodsGategories");
          let goods_for_save_list = [] as ICategorizedGoods[];
          for (let cat of this.goods_cat_list) {
              if (cat.checked) {
                  goods_for_save_list.push({
                      goods_id: this.currentGoods.id,
                      cat_id: cat.id
                  })
              }
          }
          console.log(
              "goods_for_save_list: ", goods_for_save_list
          );
          console.log("typeof this.currentGoodsID:", typeof this.currentGoodsID);
          try {
              let response = await GoodsDataService.updateCategory(
                this.currentGoodsID, goods_for_save_list, this.authToken
              );
              console.log("saveGategorizedGoods response.data", response.data);
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
            for (let good_cat of this.currentGoods.categories){
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