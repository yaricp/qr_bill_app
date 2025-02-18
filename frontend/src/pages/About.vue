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
      <div class="row">
          <div class="col">
            {{ $t("about.text5") }}
            <p></p>
          </div> 
      </div>

      <div class="row">
        <div class="col">
            <a data-bs-toggle="collapse" href="#collapseExample1" role="button" aria-expanded="false" aria-controls="collapseExample">
                <b>{{ $t("about.capabilities.header") }}</b>
            </a>
            <div class="collapse" id="collapseExample1">
                <p></p>
                <p>
                    {{ $t("about.capabilities.text1") }}
                </p>
                <p>
                    {{ $t("about.capabilities.text2") }}
                </p>
                <p>
                    {{ $t("about.capabilities.text3") }}
                </p>
                <p>
                    {{ $t("about.capabilities.text4") }}
                </p>
                <p>
                    {{ $t("about.capabilities.text5") }}
                </p>
                <p>
                    {{ $t("about.capabilities.text6") }}
                    &nbsp;
                    <a href="https://t.me/qracun_bot" target="blank">
                        @qracun_bot
                    </a>
                </p>
                <p>
                    {{ $t("about.capabilities.text7") }}
                </p>
            </div>
            <p></p>
        </div>
      </div>
      <div class="row">
        <div class="col">
            <a data-bs-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false" aria-controls="collapseExample">
                <b>{{ $t("about.why.header") }}</b>
            </a>
            <div class="collapse" id="collapseExample2">
                <p></p>
                <p>
                    {{ $t("about.why.text1") }}
                </p>
                <p>
                    {{ $t("about.why.text2") }}
                </p>
                <p>
                    {{ $t("about.why.text3") }}
                </p>
            </div>
            <p></p>
        </div>
      </div>
      <div class="row">
        <div class="col">
            <a data-bs-toggle="collapse" href="#collapseExample3" role="button" aria-expanded="false" aria-controls="collapseExample">
                <b>{{ $t("about.pwa.header") }}</b>
            </a>
            <div class="collapse" id="collapseExample3">
                <p></p>
                <p>
                    {{ $t("about.pwa.text1") }}
                </p>
                <p>
                    {{ $t("about.pwa.text2") }}
                </p>
                <p>
                    {{ $t("about.pwa.text3") }}
                </p>
                <p>
                    {{ $t("about.pwa.text4") }}
                </p>
            </div>
            <p></p>
        </div>
      </div>
      <div class="row">
        <div class="col">
            <a data-bs-toggle="collapse" href="#collapseExample4" role="button" aria-expanded="false" aria-controls="collapseExample">
                <b>{{ $t("about.security.header") }}</b>
            </a>
            <div class="collapse" id="collapseExample4">
                <p></p>
                <p>
                    {{ $t("about.security.text1") }}
                </p>
                <p>
                    {{ $t("about.security.text2") }}
                </p>
                <p>
                    {{ $t("about.security.text3") }}
                </p>
                <p>
                    {{ $t("about.security.text4") }}
                </p>
                <p>
                    {{ $t("about.security.text5") }}
                </p>
                <p>
                    {{ $t("about.security.text6") }}
                </p>
                <p>
                    {{ $t("about.security.text7") }}
                </p>
            </div>
            <p></p>
        </div>
      </div>
      <div class="row">
        <div class="col">
            <a data-bs-toggle="collapse" href="#collapseExample5" role="button" aria-expanded="false" aria-controls="collapseExample">
                <b>{{ $t("about.contacts.header") }}</b>
            </a>
            <div class="collapse" id="collapseExample5">
                <p></p>
                <p>
                    {{ $t("about.contacts.text1") }}   
                </p>
                <p>
                    {{ $t("about.contacts.text2") }}
                    &nbsp;
                    <a href="https://t.me/qracun_me_news" target="blank">
                        @qracun_me_news
                    </a>
                </p>
                <p>
                    {{ $t("about.contacts.text3") }}
                    &nbsp;
                    <a href="https://www.threads.net/@qracun.me" target="blank">
                        qracun.me
                    </a>
                </p>
                <p>
                    {{ $t("about.contacts.text4") }}
                    &nbsp;
                    <a href="https://www.instagram.com/qracun.me/" target="blank">
                        qracun.me
                    </a>
                </p>
                <p>
                    {{ $t("about.contacts.text5") }}
                    &nbsp;
                    <a href="https://t.me/+JTmkic8XatMxMzI6" target="blank">
                        Telegram-чат
                    </a>
                </p>
                <p>
                    {{ $t("about.contacts.text6") }}
                </p>
            </div>
            <p></p>
        </div>
      </div>

      <div class="row">
        <div class="col">
            <p style="color:red;">
                {{ $t("about.attention.header") }}
            </p>
        </div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.attention.text1") }}</div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.attention.text2") }}</div>
      </div>
      <div class="row">
          <div class="col">{{ $t("about.attention.text3") }}</div>
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