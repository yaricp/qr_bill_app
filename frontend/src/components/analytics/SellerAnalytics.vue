<template>
    <div>
      <h4>{{ main_header }}</h4>
      <p></p>
      <hr>
      <p></p>
      <p>{{ plot_header_by_count_bills }}</p>
      <p>
        First from all: 
        <input v-model="first_of_by_count_bills">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountBillsByNameSeller"
        >Start</button>
      </p>
      <Bar
        v-if="loaded_by_count_bills"
        id="my-chart-id1"
        :options="chartOptions"
        :data="chartDataCountBillsByName"
      />
      <hr>
      <p>{{ plot_header_by_summ_bills }}</p>
      <p>
        First from all: 
        <input v-model="first_of_by_summ_bills">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataSummBillsByNameSeller"
        >Start</button>
      </p>
      <Bar
        v-if="loaded_by_summ_bills"
        id="my-chart-id2"
        :options="chartOptions"
        :data="chartDataSummBillsByName"
      />
      <hr>
      <p>{{ plot_header_by_quantity_goods }}</p>
      <p>
        First from all: 
        <input v-model="first_of_by_quantity_goods">
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="fillChartDataCountGoodsByNameSeller"
        >Start</button>
      </p>
      <Bar
        v-if="loaded_by_quantity_goods"
        id="my-chart-id2"
        :options="chartOptions"
        :data="chartDataCountGoodsByName"
      />
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
      main_header: "Analytics Bills and Goods by Sellers" as string,
      plot_header_by_count_bills: "Count bills by sellers" as string,
      plot_header_by_summ_bills: "Total price bills by sellers" as string,
      plot_header_by_quantity_goods: "Total quantity goods by sellers" as string,
      loaded_by_count_bills: false as boolean,
      loaded_by_summ_bills: false as boolean,
      loaded_by_quantity_goods: false as boolean,
      first_of_by_count_bills: 10 as number,
      first_of_by_summ_bills: 10 as number,
      first_of_by_quantity_goods: 10 as number,
      chartDataCountBillsByName: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
      },
      chartDataSummBillsByName: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
      },
      chartDataCountGoodsByName: {
        labels: [ 'January', 'February', 'March' ],
        datasets: [ { data: [40, 20, 12] } ]
      },
      chartOptions: {
        responsive: true
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