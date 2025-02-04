<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <strong>{{ $t('profile.change_lang')}}</strong>
            </div>
            <div class="col">
                <div class="locale-changer">
                    <select 
                        v-model="$i18n.locale"
                        @change="langChanged()"
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
    },
    methods: {
        langChanged(){
            this.$i18n.locale = this.lang;
        }
    }
  })
  </script>