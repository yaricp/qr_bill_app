<template>
  <div class="list row">
    <div class="col-md-8">
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by name"
          v-model="search_name"
        />
        <div class="input-group-append">
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="searchName"
          >
            Search
          </button>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <b-button
        class="btn btn-outline-secondary"
        type="button"
        @click="showNewCategory"
      >
        Add
      </b-button>
      <b-button id="show-btn" @click="$bvModal.show('bv-modal-example')">
        Open Modal
      </b-button>
    </div>
    <div class="col-md-6">
      <h4>Categories List</h4>
      <ul class="list-group">
        <li
          class="list-group-item"
          :class="{ active: index == currentIndex }"
          v-for="(cat, index) in cat_list"
          :key="index"
          @click="setActiveCat(cat, index)"
        >
          {{ cat.name }}
        </li>
      </ul>

    </div>
    <div class="col-md-6">
      <div v-if="currentCat.id">
        <h4>Tutorial</h4>
        <div>
          <label><strong>Name:</strong></label> 
          {{ currentCat.name }}
        </div>

        <router-link
          :to="currentCat.id"
          class="badge badge-warning"
          >Edit</router-link
        >
      </div>
      <div v-else>
        <br />
        <p>Please click on a Categories...</p>
      </div>
    </div>
  </div>
</template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import CategoriesService from "@/services/categories";
  import { ICategory } from "@/interfaces/categories";
  import ResponseData from "@/interfaces/ResponseData";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";

  
  export default defineComponent({
    name: "categories-list",
    data() {
      return {
        cat_list: [] as ICategory[],
        currentCat: {} as ICategory,
        currentIndex: -1,
        new_name_category: "",
        search_name: "",
        showedCreateCategoryForm: false
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
      searchName() {
        CategoriesService.findByName(
          this.search_name, this.authToken
        )
          .then((response: ResponseData) => {
            this.cat_list = response.data;
            this.setActiveCat({} as ICategory);
            console.log(response.data);
          })
          .catch((e: Error) => {
            console.log(e);
          });
      },
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