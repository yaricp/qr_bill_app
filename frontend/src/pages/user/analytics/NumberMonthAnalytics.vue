<template>
  <div class="container">
    <div class="row">
      <center>{{ $t("main.number_month.header") }}</center>
    </div>
    <div class="row">
      <div class="col">
        <center><h1>{{ summ_month }}</h1></center>
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