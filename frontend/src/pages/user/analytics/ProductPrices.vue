<template>
    <div class="container">
      <div class="row">
        <div class="col">
          <h4>{{ $t("product_prices.header") }}</h4>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <hr>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <select 
          class="form-select"
          aria-label="Default select example"
          @change="productSelected"
          v-model="currentProduct"
        >
          <option selected>
            {{ $t("product_prices.selection_tip") }}
          </option>
          <option 
            v-for="(product, index) in products"
            :key="index"
            :value="product"
          >
            {{ product.name }}
          </option>
        </select>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <hr>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <ChartLine
            v-if="loaded"
            id="my-chart-id2"
            :options="chartOptions"
            :data="chartData"
          />
        </div>
      </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import { Line as ChartLine } from "vue-chartjs";
import { 
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  CategoryScale,
  LinearScale,
  LineElement
 } from "chart.js";

import { useStore } from "@/store";
import { Colors } from "@/constants";
import { checkTokenExpired } from "@/http-common";
import ProductDataService from "@/services/products";
import { IProduct, IProductPrice } from "@/interfaces/product";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default defineComponent({
  name: "products-prices-page",
  components: { ChartLine },
  data() {
    return {
      loaded: false,
      products: [] as IProduct[],
      currentProduct: {} as IProduct,
      chartData: {
        labels: [ "" ],
        datasets: [{ backgroundColor: Colors, data: [0], label: "" }]
      },
      chartOptions: {
        responsive: true
      },
      product_prices: [] as IProductPrice[],
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
    async retrieveProducts() {
      try {
        let response = await ProductDataService.getAll(
          this.authToken
        );
        this.products = response.data.sort(
          (a: any, b: any) => a.name.localeCompare(b.name)
        );
        console.log("response.data: ", response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async retrieveProductPrices() {
      try {
        let response = await ProductDataService.getProductPrices(
          this.currentProduct.id, this.authToken
        );
        this.product_prices = response.data;
        console.log("response.data: ", response.data);
      } catch(e) {
        checkTokenExpired(e);
      }
    },
    async fillChart() {
      let labels = [] as Array<string>;
      let prices = [] as Array<number>;
      for (const item of this.product_prices) {
        console.log("item: ", item);
        labels.push(item.created);
        prices.push(item.price);
      }
      this.chartData.datasets[0].data = prices;
      this.chartData.datasets[0].label = this.currentProduct.name;
      this.chartData.labels = labels;
      await this.$nextTick();
    },
    async productSelected() {
      this.loaded = false;
      await this.retrieveProductPrices();
      await this.fillChart();
      this.loaded = true;
    }
  },
  async mounted() {
    await this.retrieveProducts();
  }

});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>