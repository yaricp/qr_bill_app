<template>
  <div class="container">
    <div class="row">
        <div class="col">
            <strong>{{ $t('change_lang')}}</strong>
        </div>
        <div class="col">
            <div class="locale-changer">
                <select 
                    v-model="$i18n.locale"
                >
                    <option 
                        v-for="locale in $i18n.availableLocales" 
                        :key="`locale-${locale}`" 
                        :value="locale">{{ $t("lang." + locale) }}
                    </option>
                </select>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col">
            <center><h2>{{ $t("agreement.header")}}</h2></center>
        </div>
    </div>
    <div class="row">
        <div class="col"></div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "agreement-page",
    data() {
        return {
            lang: "en" as string,
        }
    }
  })
  </script>