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
        <table id="tableComponent"
            class="table table-bordered table-striped"
        >
            <thead>
                <tr>
                    <th  
                        v-for="(field, key) in fields"
                        :key="key"
                        @click="sortTable(field)" 
                    > 
                        {{ $t("table.fields."+field) }} 
                        <span v-if="field != 'ID'">
                            <svg v-if="!reverseSorted" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-up" viewBox="0 0 16 16">
                            <path d="M3.5 12.5a.5.5 0 0 1-1 0V3.707L1.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.5.5 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L3.5 3.707zm3.5-9a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                            </svg>
                            <svg v-if="reverseSorted" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-sort-down" viewBox="0 0 16 16">
                                <path d="M3.5 2.5a.5.5 0 0 0-1 0v8.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L3.5 11.293zm3.5 1a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5M7.5 6a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm0 3a.5.5 0 0 0 0 1h1a.5.5 0 0 0 0-1z"/>
                            </svg>
                        </span>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in displayedItems" :key="item">
                    <td 
                        v-for="(field, key) in fields" :key="key"
                    >
                        <div v-if="!isFieldID(field)">
                            <a :href="'/bill_photo/' + item[field]"
                                v-if="item[field] && field=='Image'" 
                            >Photo</a>
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
        <div v-if="showPaginator" class="row">
            <div class="col">
                <button
                    class="btn btn-outline-secondary"
                    type="button"
                    v-if="currentPage != 1"
                    @click="previous"
                > {{ $t("paginator.prev") }} </button>
            </div>
            <div class="col">
                {{ currentPage }} &nbsp; 
                {{ $t("paginator.page") }} &nbsp;
                {{ $t("paginator.from") }} &nbsp;
                {{ pageCount }}
            </div>
            <div class="col">
                <button
                    class="btn btn-outline-secondary"
                    type="button"
                    v-if="currentPage != pageCount"
                    @click="next"
                > {{ $t("paginator.next") }} </button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { 
    defineComponent,
    SetupContext,
    watch, ref, 
    computed,
    onMounted
} from "vue";
import { orderBy } from "lodash";
import i18n from "@/plugins/i18n";
import { boolean, string } from "yup";
import { useRouter } from 'vue-router';

interface Props {
    items?: Array<Object>;
    go_to_object?: string;
    fields?: Array<string>;
    field_search?: string;
    translate_first_column?: boolean;
    show_paginator?: boolean;
}

export default defineComponent({
    name: 'table-component-page',
    props: {
        go_to_object: { type: string },
        items: { type: Array<Object> },
        fields: { type: Array<string> },
        field_search: { type: string },
        translate_first_column: { type: boolean },
        show_paginator: { type: boolean }
    },
    setup(props: Props, context: SetupContext) {

        const router = useRouter()
        let showSearch = ref(false);
        const search_name = ref("");
        let reverseSorted = ref(false);
        const showPaginator = ref(false);
        let inner_data: any = ref([]);
        const itemsPerPage = ref(10);
        const currentPage = ref(1);
        
        
        watch(() => props.items, (first, second) => {
            if (first) {
                console.log("watch props.items: ", props.items);
                inner_data.value = first;
            }
        });

        const pageCount = computed(() => 
            Math.ceil(
                (inner_data.value ? inner_data.value.length : 0)  / itemsPerPage.value
            )
        );

        const pages = computed(() => {
            return Array.from(
                { length: pageCount.value }, (_, i) => i + 1
            );
        });

        const displayedItems = computed(() => {
            // console.log("displayedItems inner_data.value: ", inner_data.value);
            const startIndex = (currentPage.value - 1) * itemsPerPage.value;
            const endIndex = startIndex + itemsPerPage.value;
            if (inner_data.value){
                return inner_data.value.slice(startIndex, endIndex);
            }
            return [];
        });

        const changePage = (pageNumber: number) => {
            currentPage.value = pageNumber;
        };

        const sortTable = (col: any) => {
            console.log("col: ", col)
            changePage(1);
            search_name.value = "";
            let direction: "asc" | "desc" | undefined = "asc";
            if (reverseSorted.value) {
                reverseSorted.value = false;
                direction = "asc"
            } else {
                reverseSorted.value = true;
                direction = "desc"
            }
            if (col == "Created") {
                if (inner_data.value){
                    inner_data.value.sort(
                        (a: any, b: any ) => {
                            let in_a = a.Created;
                            let in_b = b.Created;
                            if (i18n.global.locale == "ru"){
                                in_a = convertFromRussianDatetime(a.Created)
                                in_b = convertFromRussianDatetime(b.Created)
                            }
                            if (direction == "desc"){
                                return Date.parse(in_a) - Date.parse(in_b)
                            } else {
                                return Date.parse(in_b) - Date.parse(in_a)
                            }
                            
                        }
                    );
                } else {
                    inner_data.value = [];
                }
            } else {
                inner_data.value = orderBy(
                    props.items, col, direction
                )
            }
        };

        const goToDetail = (id: string) => {
            router.push({
                name: String(props.go_to_object),
                params: {id: id}
            });
        };

        const getPhotoUrl = (id: string) => {
            return "bill_photo/"+id;
        };
        
        const filterData = () => {
            if (!props.items){
                return;
            };
            console.log("filterData");
            changePage(1);
            inner_data.value = props.items.filter(
                (item: any) => {return (
                    item[String(props.field_search)].toLowerCase().indexOf(
                        search_name.value.toLowerCase()
                    ) != -1
                )}
            )
        };

        const isImage = (item: any) => {
            if(
                item 
                && typeof item == "string"
                && item.includes("data:image/jpeg")
            ){
                return true;
            } else {
                return false;
            }
        };

        const isFieldID = (field: string)=> {
            if (field == "ID"){
                return true;
            }
            return false;
        };

        const convertFromRussianDatetime = (datetime: string) => {
            let time = datetime.split(" ")[1]
            let day = datetime.split(" ")[0].split(".")[0];
            let month = datetime.split(" ")[0].split(".")[1];
            let year = datetime.split(" ")[0].split(".")[2];
            return `${month}/${day}/${year} ${time}`
        };

        const previous = () => {
            // console.log("currentPage.value: ", currentPage.value);
            if (currentPage.value > 1) {
                currentPage.value = currentPage.value - 1;
            }
            // console.log("currentPage.value: ", currentPage.value);
        };

        const next = () => {
            // console.log("currentPage.value: ", currentPage.value);
            if (currentPage.value >= 1 && currentPage.value < pageCount.value) {
                currentPage.value = currentPage.value + 1;
            }
            // console.log("currentPage.value: ", currentPage.value);
        };

        onMounted(() => {
            if (props.field_search){
                showSearch.value = true;
            }
            if (props.show_paginator){
                showPaginator.value = true;
            }
            console.log("mount props.items: ", props.items);
            if (props.items){
                inner_data.value = props.items;
            }
        });

        return {
            convertFromRussianDatetime,
            filterData, goToDetail, sortTable, getPhotoUrl,
            isImage, isFieldID, next, previous, pageCount,
            displayedItems, changePage, pages, itemsPerPage,
            currentPage, reverseSorted, search_name, showPaginator
        };  
    }
})
</script>