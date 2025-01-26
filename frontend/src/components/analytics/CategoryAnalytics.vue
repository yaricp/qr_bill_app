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
      <div class="col-md-11">
        {{ $t("analytics.cat.options") }}
      </div>
      <div class="col-md-1">
        <button 
          v-if="showedOptions"
          class="btn btn-outline-secondary"
          @click="showedOptions=!showedOptions"
        >
          -
        </button>
        <button 
          v-if="!showedOptions"
          class="btn btn-outline-secondary"
          type="button"
          @click="showedOptions=!showedOptions"
        >
          +
        </button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <hr>
      </div>
    </div>
    <div class="row" v-if="showedOptions">
      <div class="col">
        <p>
          {{ $t("analytics.cat.show_by_month") }}&nbsp;
          <input 
            class="form-check-input" 
            type="checkbox" 
            v-model="showedByMonths" 
            id="flexCheckedAll"
            @change="byMonthsChecked"
          >
        </p>
      </div>
      <div class="col" v-if="showedByMonths">
        <p>{{ $t("analytics.cat.month") }}&nbsp;&nbsp;{{ getCurrentMonthName() }}</p>
      </div>
    </div>
    <div class="row" v-if="showedOptions">
      <div class="col">
        <hr>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <p>
          {{ plot_header_by_summ }}&nbsp;
          <span v-if="showedByMonths">for {{ getCurrentMonthName() }}</span> 
        </p>
      </div>
    </div>
    <div class="row" v-if="showedOptions">
      <div class="col">
        <p>
          {{ $t("analytics.cat.first_by_summ") }}&nbsp;
          <input v-model="first_of_by_summ" size="3">&nbsp;
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="fillChartDataSummByName"
          >{{ $t("analytics.cat.btn_update") }}</button>
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Bar
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
        <p>
          {{ plot_header_by_count }}&nbsp;
          <span v-if="showedByMonths">for {{ getCurrentMonthName() }}</span> 
        </p>
      </div>
    </div>
    <div class="row" v-if="showedOptions">
      <div class="col">
        <p>
          {{ $t("analytics.cat.first_by_count") }}&nbsp;
          <input v-model="first_of_by_count" size=3>&nbsp;
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="fillChartDataCountByName"
          >{{ $t("analytics.cat.btn_update") }}</button>
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <Bar
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
import { defineComponent } from "vue";
import CategoryDataService from "@/services/categories";
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
      main_header: this.$t("analytics.cat.header.main") as string,
      plot_header_by_count: this.$t("analytics.cat.header.by_count") as string,
      plot_header_by_summ: this.$t("analytics.cat.header.by_summ") as string,
      loaded_by_count: false,
      loaded_by_summ: false,
      showedByMonths: false as boolean,
      showedOptions: false as boolean,
      choosen_month: "curr" as string,
      delta_month: 1 as number,
      first_of_by_count: 10 as number,
      first_of_by_summ: 10 as number,
      chartDataCountByName: {
        labels: [''],
        datasets: [{
          label: this.$t("analytics.cat.plot_count.label"),
          data: [0]
        }]
      },
      chartDataSummByName: {
        labels: [''],
        datasets: [{
          label: this.$t("analytics.cat.plot_summ.label"),
          data: [0]
        }]
      },
      chartOptions: {
        responsive: true
      },
      goods_list_by_count: [] as ICountSellerByName[],
      goods_list_by_summ: [] as ISummSellerByName[],
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
    async retrieveCountGoodsByNameCategories() {
      try {
        let response = await CategoryDataService.getCountGoodsByNameCategory(
          this.first_of_by_count, this.delta_month, this.authToken
        );
        this.goods_list_by_count = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async retrieveSummGoodsByNameCategories() {
      try {
        let response = await CategoryDataService.getSummGoodsByNameCategory(
          this.first_of_by_summ, this.delta_month, this.authToken
        );
        this.goods_list_by_summ = response.data;
        console.log(response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async fillChartDataCountByName() {
      this.loaded_by_count = false;
      await this.retrieveCountGoodsByNameCategories();
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
      await this.retrieveSummGoodsByNameCategories();
      let summ_goods_by_name_labels = [] as Array<string>;
      let summ_goods_by_name_values = [] as Array<number>;
      for (const item of this.goods_list_by_summ) {
        summ_goods_by_name_labels.push(item["name"]);
        summ_goods_by_name_values.push(item["summ"]);
      }
      this.chartDataSummByName.datasets[0].data = summ_goods_by_name_values;
      this.chartDataSummByName.labels = summ_goods_by_name_labels;
      this.loaded_by_summ = true;
    },
    async byMonthsChecked() {
      if (this.showedByMonths){
        this.delta_month = 0;
      } else {
        this.delta_month = 1;
      }
      await this.fillChartDataCountByName();
      await this.fillChartDataSummByName();
    },
    getCurrentMonthName(delta_month?: number){
      const month = [
        "January","February","March","April","May",
        "June","July","August","September","October",
        "November","December"
      ];
      if (this.delta_month == 0){
        let d = new Date();
        return month[d.getMonth()];
      }  
    }
  },
  async mounted() {
    console.log("this.$route.params: ", this.$route.params);

    let by_months = this.$route.params.by_months;
      if (typeof by_months == "string") {
        console.log("by_months: ", by_months);
        if (by_months == "1") {
          this.showedByMonths = true;
          this.delta_month = 0;
        }
      }
    await this.$nextTick();
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