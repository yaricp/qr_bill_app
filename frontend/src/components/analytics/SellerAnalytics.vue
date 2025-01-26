<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h4>{{ main_header }}</h4>
      </div>
    </div> 
    <div class="row">
      <div class="col">
        <hr/>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>{{ plot_header_by_summ_bills }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        {{ $t("analytics.sellers.first_by_summ") }}&nbsp; 
        <input v-model="first_of_by_summ_bills" size="3">&nbsp;
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataSummBillsByNameSeller"
        >{{ $t("analytics.sellers.btn_update") }}</button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Bar
          v-if="loaded_by_summ_bills"
          id="my-chart-id2"
          :options="chartOptions"
          :data="chartDataSummBillsByName"
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
        <p>{{ plot_header_by_count_bills }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        {{ $t("analytics.sellers.first_by_count") }}&nbsp;
        <input v-model="first_of_by_count_bills" size="3">&nbsp;
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountBillsByNameSeller"
        >{{ $t("analytics.sellers.btn_update") }}</button>
      </div>
    </div> 
    <div class="row">
      <div class="col">
        <Bar
          v-if="loaded_by_count_bills"
          id="my-chart-id1"
          :options="chartOptions"
          :data="chartDataCountBillsByName"
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
        <p>{{ plot_header_by_quantity_goods }}</p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        {{ $t("analytics.sellers.first_goods_by_summ") }}&nbsp; 
        <input v-model="first_of_by_quantity_goods" size="3">&nbsp;
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountGoodsByNameSeller"
        >{{ $t("analytics.sellers.btn_update") }}</button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Bar
          v-if="loaded_by_quantity_goods"
          id="my-chart-id2"
          :options="chartOptions"
          :data="chartDataCountGoodsByName"
        />
      </div>
    </div>  
  </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import SellerDataService from "@/services/sellers";
import { ICountSellerByName, ISummSellerByName } from "@/interfaces/seller";
import { Bar } from 'vue-chartjs';
import { useStore } from '@/store';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { checkTokenExpired } from "@/http-common";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
  name: "analitics-page",
  components: { Bar },
  data() {
    return {
      main_header: this.$t("analytics.sellers.header.main") as string,
      plot_header_by_count_bills: this.$t("analytics.sellers.header.by_count_bills") as string,
      plot_header_by_summ_bills: this.$t("analytics.sellers.header.by_summ_bills") as string,
      plot_header_by_quantity_goods: this.$t("analytics.sellers.header.by_count_goods") as string,
      loaded_by_count_bills: false as boolean,
      loaded_by_summ_bills: false as boolean,
      loaded_by_quantity_goods: false as boolean,
      first_of_by_count_bills: 10 as number,
      first_of_by_summ_bills: 10 as number,
      first_of_by_quantity_goods: 10 as number,
      chartDataCountBillsByName: {
        labels: [""],
        datasets: [ { 
          label: this.$t("analytics.sellers.plot_count.label"),
          data: [0]
         } ]
      },
      chartDataSummBillsByName: {
        labels: [""],
        datasets: [ { 
          label: this.$t("analytics.sellers.plot_summ.label"),
          data: [0]
        } ]
      },
      chartDataCountGoodsByName: {
        labels: [""],
        datasets: [ { 
          label: this.$t("analytics.sellers.plot_goods.label"),
          data: [0] 
        } ]
      },
      chartOptions: {
        responsive: true,
        onClick: this.chartOnClick
      },
      bills_list_by_count: [] as ICountSellerByName[],
      bills_list_by_summ: [] as ISummSellerByName[],
      goods_list_by_quantity: [] as ICountSellerByName[],
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
    async retrieveCountBillsByNameSeller() {
      try {
        let response = await SellerDataService.getCountBillsByNameSeller(
          this.first_of_by_count_bills, this.authToken
        );
        this.bills_list_by_count = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async retrieveSummBillsByNameSeller() {
      try {
        let response = await SellerDataService.getSummBillsByNameSeller(
          this.first_of_by_summ_bills, this.authToken
        );
        this.bills_list_by_summ = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async retrieveCountGoodsByNameSeller() {
      try {
        let response = await SellerDataService.getCountGoodsByNameSeller(
          this.first_of_by_quantity_goods, this.authToken
        );
        this.goods_list_by_quantity = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async fillChartDataCountBillsByNameSeller() {
      this.loaded_by_count_bills = false;
      await this.retrieveCountBillsByNameSeller();
      let count_bills_by_name_labels = [] as Array<string>;
      let count_bills_by_name_values = [] as Array<number>;
      for (const item of this.bills_list_by_count) {
        count_bills_by_name_labels.push(item["name"]);
        count_bills_by_name_values.push(item["count"]);
      }
      this.chartDataCountBillsByName.datasets[0].data = count_bills_by_name_values;
      this.chartDataCountBillsByName.labels = count_bills_by_name_labels;
      this.loaded_by_count_bills = true;
    },
    async fillChartDataSummBillsByNameSeller() {
      this.loaded_by_summ_bills = false;
      await this.retrieveSummBillsByNameSeller();
      let summ_bills_by_name_labels = [] as Array<string>;
      let summ_bills_by_name_values = [] as Array<number>;
      for (const item of this.bills_list_by_summ) {
        summ_bills_by_name_labels.push(item["name"]);
        summ_bills_by_name_values.push(item["summ"]);
      }
      this.chartDataSummBillsByName.datasets[0].data = summ_bills_by_name_values;
      this.chartDataSummBillsByName.labels = summ_bills_by_name_labels;
      this.loaded_by_summ_bills = true;
    },
    async fillChartDataCountGoodsByNameSeller() {
      this.loaded_by_quantity_goods = false;
      await this.retrieveCountGoodsByNameSeller();
      let count_goods_by_name_labels = [] as Array<string>;
      let count_goods_by_name_values = [] as Array<number>;
      for (const item of this.goods_list_by_quantity) {
        count_goods_by_name_labels.push(item["name"]);
        count_goods_by_name_values.push(item["count"]);
      }
      this.chartDataCountGoodsByName.datasets[0].data = count_goods_by_name_values;
      this.chartDataCountGoodsByName.labels = count_goods_by_name_labels;
      this.loaded_by_quantity_goods = true;
    },
    chartOnClick1(evt: any) {
      let chart = evt.chart
      const points = chart.getElementsAtEventForMode(
        evt, 'nearest', {}, true
      );
      
      if (points.length) {
        const firstPoint = points[0];
        //var label = myChart.data.labels[firstPoint.index];
        //var value = myChart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
        let datasetIndex = firstPoint.datasetIndex, index = firstPoint.index;
        
        if (firstPoint.element.hidden != true) {
            chart.hide(datasetIndex, index);
        } else {
            chart.show(datasetIndex, index);
        }
        // chart.data.datasets[0].data.splice(index, 1);
        // chart.update();
        // let meta = chart.getDatasetMeta(datasetIndex).data[index];

        // // toggle visibility of index if exists
        // if (meta) {
        //   meta.hidden = !meta.hidden;
        // }
      }
    }
  },
  async mounted() {
    this.fillChartDataCountBillsByNameSeller();
    this.fillChartDataSummBillsByNameSeller(); 
    this.fillChartDataCountGoodsByNameSeller();
  }

});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>