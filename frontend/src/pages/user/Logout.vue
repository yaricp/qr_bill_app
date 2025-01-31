
<script lang="ts">
import { defineComponent } from "vue"
import { useRouter } from "vue-router"
import { useStore } from '@/store';

export default defineComponent({
    name: "logout-page",
    async created() {
        try {
            let result = await this.$store.dispatch("auth/logout");
            console.log(result);
            this.$router.push({ name: 'login' })
        } catch(e) {
            console.log(e);
        }
    }
})
</script>