<template>
  <div class="container">
    <div class="row" v-if="!cat_list">
      <div class="col">
        <h4>!{{ $t("lists.cat.empty_list_tip") }}</h4>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            :placeholder="$t('lists.cat.add_cat_placeholder')"
            v-model="new_name_category"
          />
          <div class="input-group-append">
            &nbsp;
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="addCategory"
            >
              {{ $t("lists.cat.btn_add") }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="row" v-if="cat_list">
      <h3>{{ $t("lists.cat.head") }}</h3>
    </div>
    <table id="tableComponent" class="table table-bordered table-striped">
      <thead>
          <tr>
            <th>{{ $t("table.fields.Name") }}</th>
            <th>&nbsp;</th>
            <th>{{ $t("table.fields.Actions") }}</th>
          </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(cat, index) in cat_list"
          :key="index">
          <td>
            <span v-if="!editButtonShowed(index)">
              {{ cat.name }}
            </span>
            <span v-if="editButtonShowed(index)">
              <input 
                type="text"
                class="form-control"
                v-model="currentCat.name"
              />
            </span>
          </td>
          <td>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="!editButtonShowed(index)"
              @click="showEdit(index, cat)"
            >
            {{ $t("lists.cat.btn_edit") }}
            </button>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="editButtonShowed(index)"
              @click="saveCategory(index, cat)"
            >
            {{ $t("lists.cat.btn_save") }}
            </button>
          </td>
          <td>
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="delCategory(index, cat)"
            >
            {{ $t("lists.cat.btn_del") }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
<script lang="ts">
  import { defineComponent } from "vue";
  import CategoriesService from "@/services/categories";
  import { ICategory } from "@/interfaces/categories";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";

  
  export default defineComponent({
    name: "categories-list",
    compatConfig: { MODE: 3 },
    data() {
      return {
        cat_list: [] as ICategory[],
        currentCat: {} as ICategory,
        currentIndex: -1,
        new_name_category: "",
        showedCreateCategoryForm: false as boolean,
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
          this. cat_list = response.data;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async addCategory() {
        try {
          let data = {"name": this.new_name_category}
          let response = await CategoriesService.create(
            data,
            this.authToken
          );
          this.cat_list.push(response.data);
          console.log(response.data);
          this.new_name_category = "";
          // this.refreshList();
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      showNewCategory() {
        this.showedCreateCategoryForm = true;
      },
      refreshList() {
        this.retrieveCategories();
        this.currentCat = {} as ICategory;
        this.currentIndex = -1;
      },
      setActiveCat(tutorial: ICategory, index = -1) {
        this.currentCat = tutorial;
        this.currentIndex = index;
      },
      async delCategory(index: number, cat: ICategory) {
        try {
          let response = await CategoriesService.delete(
            cat.id,
            this.authToken
          );
          this.cat_list.splice(index, 1);
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      editButtonShowed(index: number){
        if(index == this.currentIndex){
          return true;
        } else {
          return false;
        }
      },
      showEdit(index: number, cat: ICategory){
        this.currentIndex = index;
        this.currentCat = cat;
      },
      async saveCategory(index: number, cat: ICategory) {
        this.currentIndex = -1;
        try {
          let response = await CategoriesService.update(
            cat.id, cat, this.authToken
          );
          this.cat_list[index] = response.data;
          console.log(response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
        this.currentCat = {} as ICategory;
      }
    },
    mounted() {
      this.retrieveCategories();
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