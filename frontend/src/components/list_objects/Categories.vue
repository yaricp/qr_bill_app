<template>
  <div class="container">
    <div class="row" v-if="!cat_list">
      <h4>Create your own categories</h4>
    </div>
    <div class="row">
      <div class="col-md-12">
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="name of a new category"
            v-model="new_name_category"
          />
          <div class="input-group-append">
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="addCategory"
            >
              Add
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="row"><h3>Categories</h3></div>
    <table id="tableComponent" class="table table-bordered table-striped">
      <thead>
          <tr>
            <th>Name</th><th>&nbsp;</th><th>Actions</th>
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
              Edit
            </button>
            <button
              class="btn btn-outline-secondary"
              type="button"
              v-if="editButtonShowed(index)"
              @click="saveCategory(index, cat)"
            >
              Save
            </button>
          </td>
          <td>
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="delCategory(index, cat)"
            >
              Del
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