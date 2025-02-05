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
            <center><h2>{{ $t("agreement.header") }}</h2></center>
        </div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title1") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text1_1") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text1_2") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title2") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text2_1") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text2_2") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text2_3") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text2_4") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text2_5") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title3") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text3_1") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text3_2") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text3_3") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text3_4") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title4") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text4") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title5") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text5") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title6") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text6") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title7") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text7") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title8") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text8_1") }}</div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text8_2") }}</div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title9") }}</b></div>
    </div>
    <div class="row">
        <div class="col">
            {{ $t("agreement.page.text9") }}&nbsp;
            qracun@proton.me
        </div>
    </div>
    <div class="row">
        <div class="col"><b>{{ $t("agreement.page.title10") }}</b></div>
    </div>
    <div class="row">
        <div class="col">{{ $t("agreement.page.text10") }}</div>
    </div>
    <div class="row">
        <div class="col">&nbsp;</div>
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