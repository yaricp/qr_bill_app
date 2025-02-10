<template>
    <div class="container">
        <div class="searchBar" v-if="field_search">
            <!-- Filter Search -->
            <div class="input-group mb-5">
                {{ $t("filter.title") }}&nbsp;
                <input 
                    type="search" 
                    class="form-control" 
                    v-model="search_name" 
                    @keyup="filterData"
                    :placeholder="$t('filter.filter_names.' + field_search)"
                    aria-label="name"
                    aria-describedby="button-addon2">
            </div>
        </div>
        <table id="tableComponent" class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th  
                        v-for="(field, key) in fields"
                        :key="key"
                        @click="sortTable(field)" 
                    > 
                        {{ $t("table.fields."+field) }} 
                        <i class="bi bi-sort-alpha-down" aria-label='Sort Icon'></i>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in inner_data" :key="item">
                    <td 
                        v-for="(field, key) in fields" :key="key"
                    >
                        <div v-if="!isFieldID(field)">
                            <img 
                                v-if="isImage(item[field])" 
                                :src="item[field]"
                            >
                            <p v-else-if="translate_first_column && key == 0">
                                {{ $t("table.first_column." + item[field]) }}
                            </p>
                            <p v-else >
                                {{ item[field] }}
                            </p>  
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
import { defineComponent, SetupContext, watch, ref, reactive } from "vue";
import { orderBy } from 'lodash';
import { boolean, string } from "yup";

interface Props {
    items?: Array<Object>;
    go_to_object?: string;
    fields?: Array<string>;
    field_search?: string;
    translate_first_column?: boolean;
}

export default defineComponent({
    name: 'table-component-page',
    props: {
        go_to_object: { type: string },
        items: { type: Array<Object> },
        fields: { type: Array<string> },
        field_search: { type: string },
        translate_first_column: { type: boolean }
    },
    data: () => {
        return {
            showSearch: false as boolean,
            search_name: "" as string,
            reverseSorted: false as boolean,
            inner_data: [] as Object[] | undefined,
            inner_fields: [] as string[] | undefined
        }
    },
    setup(props: Props, context: SetupContext) {
        
        let showSearch = ref(false);
        let search_name = ref("");
        let reverseSorted = ref(false);
        let inner_data: Object[] | undefined = reactive([]);
        let inner_fields: string[] | undefined = reactive([]);

        watch(() => props.items, (first, second) => {
            inner_data = first;
        });
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
        convertFromRussianDatetime(datetime: string){
            let time = datetime.split(" ")[1]
            let day = datetime.split(" ")[0].split(".")[0];
            let month = datetime.split(" ")[0].split(".")[1];
            let year = datetime.split(" ")[0].split(".")[2];
            return `${month}/${day}/${year} ${time}`
        },
        sortTable(col: any) {
            console.log("col: ", col)
            this.search_name = "";
            let direction: "asc" | "desc" | undefined = "asc";
            if (this.reverseSorted) {
                this.reverseSorted = false;
                direction = "asc"
            } else {
                this.reverseSorted = true;
                direction = "desc"
            }
            if (col == "Created") {
                if (this.inner_data){
                    this.inner_data.sort(
                        (a: any, b: any ) => {
                            let in_a = a.Created;
                            let in_b = b.Created;
                            if (this.$i18n.locale == "ru"){
                                in_a = this.convertFromRussianDatetime(a.Created)
                                in_b = this.convertFromRussianDatetime(b.Created)
                            }
                            if (direction == "desc"){
                                return Date.parse(in_a) - Date.parse(in_b)
                            } else {
                                return Date.parse(in_b) - Date.parse(in_a)
                            }
                            
                        }
                    );
                } else {
                    this.inner_data = [];
                }
            } else {
                this.inner_data = orderBy(
                    this.items, col, direction
                )
            }
        },
        goToDetail(id: string){
            this.$router.push({
                name: String(this.go_to_object),
                params: {id: id}
            });
        },
        filterData(){
            if (!this.$props.items){
                return;
            };
            console.log("filterData");
            this.inner_data = this.$props.items.filter(
                (item: any) => {return (
                    item[String(this.$props.field_search)].toLowerCase().indexOf(
                        this.search_name.toLowerCase()
                    ) != -1
                )}
            )
        },
        updateInnerData(){
            this.inner_data = this.$props.items;
        }
    },
    mounted() {
        if (this.$props.field_search){
            this.showSearch = true;
        }
        this.inner_data = this.$props.items;
    }
})
</script>