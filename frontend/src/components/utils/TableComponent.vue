<template>
    <div>
        <div class="searchBar">
            <!-- Filter Search -->
            <div class="input-group mb-5">
                <input 
                    type="search" 
                    class="form-control" 
                    v-model="search_name" 
                    @keyup="filterData"
                    placeholder="Name" 
                    aria-label="name"
                    aria-describedby="button-addon2">
            </div>
        </div>
        <table id="tableComponent" class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th  
                        v-for="field in fields"
                        :key="field"
                        @click="sortTable(field)" 
                    > 
                        {{ field }} 
                        <i class="bi bi-sort-alpha-down" aria-label='Sort Icon'></i>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in inner_data" :key="item">
                    <td 
                        v-for="field in fields" :key="field"
                    >
                        <div v-if="!isFieldID(field)">
                            <p v-if="!isImage(item[field])">{{ item[field] }}</p>
                            <img 
                                v-if="isImage(item[field])" 
                                :src="item[field]"
                            >
                        </div>
                        <div v-if="isFieldID(field)">
                            <button
                                class="btn btn-outline-secondary"
                                type="button"
                                @click="goToDetail(item[field])"
                            > >> </button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table> 
    </div>
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import { orderBy } from 'lodash';
import { string } from "yup";

// let sort = ref(false);
// let updatedList = ref([]as Array<Object>)

export default defineComponent({
    name: 'table-component-page',
    props: {
        go_to_object: { type: string },
        data: { type: Array<Object> },
        fields: { type: Array<string> },
        field_search: { type: string }
    },
    data: () => {
        return {
            search_name: "" as string,
            reverseSorted: false as boolean,
            inner_data: [] as Object[] | undefined,
            inner_fields: [] as string[] | undefined
        }
    },
    methods: {
        isImage(item: any){
            if(
                item 
                && typeof item == "string"
                && item.includes("data:image/jpeg")
            ){
                return true;
            } else {
                return false;
            }
        },
        isFieldID(field: string){
            if (field == "ID"){
                return true;
            }
            return false;
        },
        sortTable(col: any) {
            console.log("sortTable");
            console.log("typeof col:", typeof col);
            let direction: "asc" | "desc" | undefined = "asc";
            if (this.reverseSorted) {
                this.reverseSorted = false;
                direction = "asc"
            } else {
                this.reverseSorted = true;
                direction = "desc"
            }
            this.inner_data = orderBy(
                this.$props.data, col, direction
            )
        },
        goToDetail(id: string){
            this.$router.push({
                name: String(this.$props.go_to_object),
                params: {id: id}
            });
        },
        filterData(){
            if (!this.$props.data){
                return;
            }
            this.inner_data = this.$props.data.filter(
                (item: any) => {return (
                    item[String(this.$props.field_search)].toLowerCase().indexOf(
                        this.search_name.toLowerCase()
                    ) != -1
                )}
            )
        }
    },
    mounted() {
        this.inner_data = this.$props.data;
    },
})
</script>