<template>
    <div class="row">
      <div class="col">
        <hr>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <h4>{{ $t("lists.users.header") }}</h4>
        <TableComponent 
          v-if="itemsReady"
          :items="items" 
          :fields="fields"
          :field_search="field_search"
          :show_paginator="true"
        />
      </div>
    </div>
  </template>
    
    <script lang="ts">
    import { defineComponent } from "vue";
    import UserService from "@/services/users";
    import { useStore } from '@/store';
    import { checkTokenExpired } from "@/http-common";
    import { IUser } from "@/interfaces/users";
    import TableComponent from '@/components/utils/TableComponent.vue';
    
    export default defineComponent({
      name: "users-list",
      components: { TableComponent },
      data() {
        return {
          users_list: [] as IUser[],
          itemsReady: false as boolean,
          fields: [
            "Id", "Email", "Email_Verified", "Phone", "Login",
            "TG_Name", "TG_Verified", "TG_ID", "Lang", "Links"
          ],
          field_search: "Login" as string,
          items: [] as Array<Object>
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
        async retrieveUsers() {
          try {
            console.log("start retrieve users: ");
            let response = await UserService.getUsers(
                this.authToken
            );
            if (response.data){
                console.log("response.data: ", response.data)
                return response.data;
            } else {
              return [];
            }
          } catch(e) {
            checkTokenExpired(e);
          }
        },
        prepareTableItems(){
          this.itemsReady = false;
          let items = [];
          for (let user of this.users_list){
            items.push({
                "Id": user.id,
                "Email": user.email,
                "Email_Verified": user.email_verified,
                "Phone": user.phone,
                "Login": user.login,
                "TG_Name": user.tg_name,
                "TG_Verified": user.tg_verified,
                "TG_ID": user.tg_id,
                "Lang": user.lang,
                "Links": user.links,
            })
          }
          this.items = items;
          // console.log(this.items);
          this.itemsReady = true;
        }
      },
      async mounted() {
        this.users_list = await this.retrieveUsers();
        this.prepareTableItems();
      },
    });
    </script>
    
    <style>
    .list {
      text-align: left;
      max-width: 750px;
      margin: auto;
    }
    </style>