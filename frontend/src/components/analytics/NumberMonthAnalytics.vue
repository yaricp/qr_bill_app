<template>
  <div class="container">
    <div class="row">
      <center>{{ $t("main.number_month.header") }}</center>
    </div>
    <div class="row">
      <div class="col">
        <center><h1>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-currency-euro" viewBox="0 0 16 16">
            <path d="M4 9.42h1.063C5.4 12.323 7.317 14 10.34 14c.622 0 1.167-.068 1.659-.185v-1.3c-.484.119-1.045.17-1.659.17-2.1 0-3.455-1.198-3.775-3.264h4.017v-.928H6.497v-.936q-.002-.165.008-.329h4.078v-.927H6.618c.388-1.898 1.719-2.985 3.723-2.985.614 0 1.175.05 1.659.177V2.194A6.6 6.6 0 0 0 10.341 2c-2.928 0-4.82 1.569-5.244 4.3H4v.928h1.01v1.265H4v.928z"/>
          </svg>
          {{ summ_month }}
        </h1></center>
      </div>
    </div>
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import { useStore } from '@/store';
import { checkTokenExpired } from "@/http-common";
import BillDataService from "@/services/bills";

export default defineComponent({
  name: "number-analitics-page",
  data() {
    return {
      loaded: false,
      summ_month: 0 as number,
      message: "",
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
    async retrieveSummForMonth() {
      try {
        let response = await BillDataService.getSummForMonth(
          0, this.authToken
        );
        this.summ_month = Number(response.data);
        console.log(response);
      } catch(e) {
        checkTokenExpired(e);
      }
    }
  },
  async mounted() {
    this.retrieveSummForMonth();  
  }

});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>