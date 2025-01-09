<template>
    <main>
        <div><p>Test mess: {{ test_mess }}</p></div>
        <div
            v-if="html5QrcodeScanner"
        >
            <p>Status Scanner: {{ html5QrcodeScanner.getState() }}</p>
        </div>
        <div>
            <div id="qr-scanner"/>
        </div>
        <div><p>Message: {{ message }}</p></div>
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Html5QrcodeScanner } from "html5-qrcode";
import { useStore } from '@/store';
import BillDataService from "@/services/bills";
import { checkTokenExpired } from "@/http-common";
import { ICategory } from "@/interfaces/categories";

export default defineComponent({
    name: "qrscanner-page",
    data() {
        return {
            url_patterns: ["https://", "ic/", "mapr"] as Array<string>,
            qrbox: 180 as number,
            fps: 10 as number,
            test_mess: "" as string,
            message: "" as string,
            found: false as boolean,
            html5QrcodeScanner: undefined as any,
            result: {},
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
        async onScanSuccess(qrCodeMessage: string) {
            this.test_mess += qrCodeMessage;
            this.html5QrcodeScanner.pause();
            if (this.checkUrl(qrCodeMessage)){
                this.message = "Correct URL!"
            } else {
                this.message = "Wrong URL!"
            }
            this.found = true;
            let result = await this.sendUrlToServer(qrCodeMessage);
            // show found results
            this.found = false;
            this.test_mess = "";
            this.html5QrcodeScanner.resume();
        },
        checkUrl(q_message: string) {
            for (let pattern of this.url_patterns){
                if (!q_message.includes(pattern)){
                    return false;
                }
            }
            return true;
        },
        async sendUrlToServer(link: string){
            try {
                let response = await BillDataService.sendUrl(
                    {"link": link},
                    this.authToken
                );
                this.message = "sent to server successful!"
                console.log(response.data);
                return response.data
            } catch(e) {
                checkTokenExpired(e);
            }
        },
        qrboxFunction(
            viewfinderWidth: number,
            viewfinderHeight: number
        ) {
            let minEdgePercentage = 0.95; // 95% 
            let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
            let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
            return {
                width: qrboxSize,
                height: qrboxSize
            }
        }
    },
    async mounted() {
        let config = {
            fps: this.fps ? this.fps : 10,
            qrbox: this.qrboxFunction,
            aspectRatio: 3 / 2,
            disableFlip: true,
        };
        this.html5QrcodeScanner = new Html5QrcodeScanner(
            "qr-scanner", config, true
        );
        this.html5QrcodeScanner.render(
            this.onScanSuccess, undefined
        );
    }
})
</script>