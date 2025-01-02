<template>
    <div>
      <h4>Analitics</h4>
      <p>
        First from all by count: 
        <input v-model="first_of_by_count">
        <button @click="fillChartDataCountByName"/>
      </p>
      <Bar
        v-if="loaded_by_count"
        id="my-chart-id1"
        :options="chartOptions"
        :data="chartDataCountByName"
      />
      <p>
        First from all by summ: 
        <input v-model="first_of_by_summ">
        <button @click="fillChartDataSummByName"/>
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
import SellerDataService from "@/services/sellers";
import { ICountSellerByName, ISummSellerByName } from "@/interfaces/seller";
import ResponseData from "@/interfaces/ResponseData";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
  name: "analitics-page",
  components: { Bar },
  data() {
    return {
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
      goods_list_by_count: [] as ICountSellerByName[],
      goods_list_by_summ: [] as ISummSellerByName[],
      message: "",
    };
  },
  methods: {
    
    async retrieveCountSellerByName() {
      try {
        let response = await SellerDataService.getCountSellerByName(
          this.first_of_by_count
        );
        this.goods_list_by_count = response.data;
        console.log(response.data);
      } catch(e) {
        console.log(e);
      }
    },
    async retrieveSummSellerByName() {
      try {
        let response = await SellerDataService.getSummSellerByName(
          this.first_of_by_summ
        );
        this.goods_list_by_summ = response.data;
        console.log(response.data);
      } catch(e) {
        console.log(e);
      }
    },
    async fillChartDataCountByName() {
      this.loaded_by_count = false;
      await this.retrieveCountSellerByName();
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
      await this.retrieveSummSellerByName();
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