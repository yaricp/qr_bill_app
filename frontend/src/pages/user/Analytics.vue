</template>
    <div>

    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";
import GoodsDataService from "@/services/goods";
import { IGoods } from "@/interfaces/goods";
import ResponseData from "@/interfaces/ResponseData";
import { useStore } from '@/store';

export default defineComponent({
  name: "analitics-page",
  data() {
    return {
      currentGoods: {} as IGoods,
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
    getGoods(id: any) {
      GoodsDataService.get(id, this.authToken)
        .then((response: ResponseData) => {
          this.currentGoods = response.data;
          console.log(response.data);
        })
        .catch((e: Error) => {
          console.log(e);
        });
    }
  },
  mounted() {
    this.message = "";
    this.getGoods(this.$route.params.id);
  },
});
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>