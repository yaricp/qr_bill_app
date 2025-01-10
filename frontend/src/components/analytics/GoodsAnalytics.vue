<template>
    <div>
      <h4>{{ main_header }}</h4>
      <p></p>
      <hr>
      <p></p>
      <p>{{ plot_header_by_count }}</p>
      <p>
        First from all by count: 
        <input v-model="first_of_by_count">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountByName"
        >Start</button>
      </p>
      <Bar
        v-if="loaded_by_count"
        id="my-chart-id1"
        :options="chartOptions"
        :data="chartDataCountByName"
      />
      <hr>
      <p>{{ plot_header_by_summ }}</p>
      <p>
        First from all by summ: 
        <input v-model="first_of_by_summ">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataSummByName"
        >Start</button>
      </p>
      <Bar
        v-if="loaded_by_summ"
        id="my-chart-id2"
        :options="chartOptions"
        :data="chartDataSummByName"
      />
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import GoodsDataService from "@/services/goods";
import { ICountGoodsByName, ISummGoodsByName } from "@/interfaces/goods";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { useStore } from '@/store';
import { checkTokenExpired } from "@/http-common";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
  name: "analitics-page",
  components: { Bar },
  data() {
    return {
      main_header: "Analytics Goods" as string,
      plot_header_by_count: "Quantities goods by names" as string,
      plot_header_by_summ: "Total price goods by names" as string,
      loaded_by_count: false,
      loaded_by_summ: false,
      first_of_by_count: 10 as number,
      first_of_by_summ: 10 as number,
      chartDataCountByName: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
      },
      chartDataSummByName: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
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