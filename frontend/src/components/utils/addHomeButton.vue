<template>
    <div>
      <button
        class="btn btn-outline-secondary add-button"
        type="button"
        v-if="deferredPrompt"
        ref="addBtn"
        @click="clickCallback"
      >
        {{ $t("install_btn") }}
      </button>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: 'add-to-home-screen-btn',
    data: () => ({
      deferredPrompt: null as any,
    }),
    mounted() {
      this.captureEvent()
    },
    methods: {
      captureEvent() {
        window.addEventListener('beforeinstallprompt', (e) => {
          // ! Prevent Chrome 67 and earlier from automatically showing the prompt
          e.preventDefault()
          // Stash the event so it can be triggered later.
          this.deferredPrompt = e
        })
      },
      clickCallback() {
        // Show the prompt
        this.deferredPrompt.prompt()
        // Wait for the user to respond to the prompt
        this.deferredPrompt.userChoice.then(
            (choiceResult: any) => {
                if (choiceResult.outcome === 'accepted') {
                    // Call another function?
                }
                this.deferredPrompt = null
        })
      },
    },
})
</script>