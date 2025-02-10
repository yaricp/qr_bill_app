<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <center>{{ $t("main.circle.header") }}:</center>
      </div>
    </div>
    <div class="row">
      <div class="col" v-if="loaded && item_list.length != 0">
        <center>
          <Pie :data="chartData" :options="chartOptions" />
        </center>
      </div>
      <div class="col" v-if="loaded && item_list.length == 0">
        <center>
          <p style="color:red;">
            {{ $t("main.data_not_found1") }}<br>
            <router-link to="/category_products">
              {{ $t("menu.cat_goods") }}
            </router-link>
            {{ $t("main.data_not_found2") }}
            <router-link to="/categories">
              {{ $t("menu.lists.categories") }}
            </router-link>
          </p>
        </center>
      </div>
    </div>
  </div>
</template>
    
  <script lang="ts">
  import { defineComponent } from "vue";
  import { useStore } from '@/store';
  import { checkTokenExpired } from "@/http-common";
  import CategoryDataService from "@/services/categories";
  import { ISummCategoryByName } from "@/interfaces/categories";
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
  import { Pie } from "vue-chartjs";

  ChartJS.register(ArcElement, Tooltip, Legend)

  export default defineComponent({
    name: "circle-analitics-page",
    components: { Pie },
    data() {
      return {
        main_header: this.$t("analytics.cat.header.main") as string,
        plot_header: this.$t("analytics.cat.header.by_count") as string,
        loaded: false,
        first_of: 10 as number,
        chartData: {
          labels: [''],
          datasets: [{
            backgroundColor: [
              '#41A688',
              '#E46651',
              '#00D8FF',
              '#DD1B16',
              '#41B494',
              '#E46662',
              '#05F9D0',
              '#DD1A27',
              '#52C975',
              '#E46573'
            ],
            data: [0]
          }]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false
        },
        item_list: [] as ISummCategoryByName[],
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
      async retrieveSummGoodsByNameCategories() {
        try {
          let response = await CategoryDataService.getSummGoodsByNameCategory(
            this.first_of, 0, this.authToken
          );
          this.item_list = response.data;
          console.log("this.item_list: ", response.data);
        } catch(e) {
          checkTokenExpired(e);
        }
      },
      async fillChartDataSummByName() {
        this.loaded = false;
        await this.retrieveSummGoodsByNameCategories();
        let summ_goods_by_name_labels = [] as Array<string>;
        let summ_goods_by_name_values = [] as Array<number>;
        for (const item of this.item_list) {
          summ_goods_by_name_labels.push(item["name"]);
          summ_goods_by_name_values.push(item["summ"]);
        }
        console.log(
          "summ_goods_by_name_values: ", summ_goods_by_name_values
        );
        console.log(
          "summ_goods_by_name_labels: ", summ_goods_by_name_labels
        );
        this.chartData.datasets[0].data = summ_goods_by_name_values;
        this.chartData.labels = summ_goods_by_name_labels;
        this.loaded = true;
      }
    },
    async mounted() {
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