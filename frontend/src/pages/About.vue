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
              <center><h2>{{ $t("about.header") }}</h2></center>
          </div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.text1") }}</div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.text2") }}</div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.text3") }}</div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.text4") }}</div>
      </div>
    </div>
</template>
  
<script lang="ts">
    import { defineComponent } from "vue";
    
    export default defineComponent({
      name: "about-page",
      data() {
          return {
              lang: "en" as string,
          }
      }
    })
</script>