<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h4>{{ main_header }}</h4>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <hr>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>{{ plot_header_by_summ }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        {{ $t("analytics.goods.first_by_summ") }}&nbsp;
        <input v-model="first_of_by_summ" size="3">&nbsp;
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataSummByName"
        >{{ $t("analytics.goods.btn_update") }}</button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Pie
          v-if="loaded_by_summ"
          id="my-chart-id2"
          :options="chartOptions"
          :data="chartDataSummByName"
        />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <hr>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>{{ plot_header_by_count }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        {{ $t("analytics.goods.first_by_count") }}&nbsp;
        <input v-model="first_of_by_count" size="3">&nbsp;
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountByName"
        >{{ $t("analytics.goods.btn_update") }}</button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Pie
          v-if="loaded_by_count"
          id="my-chart-id1"
          :options="chartOptions"
          :data="chartDataCountByName"
        />
      </div>
    </div>
  </div>
</template>
  
<script lang="ts">
import { Pie } from "vue-chartjs";
import { defineComponent } from "vue";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

import { useStore } from "@/store";
import { Colors } from "@/constants";
import GoodsDataService from "@/services/goods";
import { checkTokenExpired } from "@/http-common";
import { ICountGoodsByName, ISummGoodsByName } from "@/interfaces/goods";

ChartJS.register(ArcElement, Tooltip, Legend)

export default defineComponent({
  name: "analitics-page",
  components: { Pie },
  data() {
    return {
      main_header: this.$t("analytics.goods.header.main") as string,
      plot_header_by_count: this.$t("analytics.goods.header.by_count") as string,
      plot_header_by_summ: this.$t("analytics.goods.header.by_summ") as string,
      loaded_by_count: false,
      loaded_by_summ: false,
      first_of_by_count: 10 as number,
      first_of_by_summ: 10 as number,
      chartDataCountByName: {
        labels: [''],
        datasets: [{ backgroundColor: Colors, data: [0] }]
      },
      chartDataSummByName: {
        labels: [''],
        datasets: [{ backgroundColor: Colors, data: [0] }]
      },
      chartOptions: {
        responsive: true
      },
      goods_list_by_count: [] as ICountGoodsByName[],
      goods_list_by_summ: [] as ISummGoodsByName[],
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
    async retrieveCountGoodsByName() {
      try {
        let response = await GoodsDataService.getCountGoodsByName(
          this.first_of_by_count, this.authToken
        );
        this.goods_list_by_count = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async retrieveSummGoodsByName() {
      try {
        let response = await GoodsDataService.getSummGoodsByName(
          this.first_of_by_summ, this.authToken
        );
        this.goods_list_by_summ = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async fillChartDataCountByName() {
      this.loaded_by_count = false;
      await this.retrieveCountGoodsByName();
      let count_goods_by_name_labels = [] as Array<string>;
      let count_goods_by_name_values = [] as Array<number>;
      for (const item of this.goods_list_by_count) {
        count_goods_by_name_labels.push(item["name"]);
        count_goods_by_name_values.push(item["count"]);
      }
      this.chartDataCountByName.datasets[0].data = count_goods_by_name_values;
      this.chartDataCountByName.labels = count_goods_by_name_labels;
      this.loaded_by_count = true;
    },
    async fillChartDataSummByName() {
      this.loaded_by_summ = false;
      await this.retrieveSummGoodsByName();
      let summ_goods_by_name_labels = [] as Array<string>;
      let summ_goods_by_name_values = [] as Array<number>;
      for (const item of this.goods_list_by_summ) {
        summ_goods_by_name_labels.push(item["name"]);
        summ_goods_by_name_values.push(item["summ"]);
      }
      this.chartDataSummByName.datasets[0].data = summ_goods_by_name_values;
      this.chartDataSummByName.labels = summ_goods_by_name_labels;
      this.loaded_by_summ = true;
    }
  },
  async mounted() {
    this.fillChartDataCountByName();
    this.fillChartDataSummByName();  
  }

});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>