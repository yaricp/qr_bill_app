<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <h3>{{ $t("scanner.head") }}</h3>
            </div>
        </div>
        <div class="row" v-if="html5QrcodeScanner">
            <div class="col">
                <p>{{ qrscannerStatusMessage }}</p>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <div ref="qr-scanner" id="qr-scanner"/>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <p>{{ message }}</p>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <img :src="picture" />
            </div>
        </div>
        <!-- <div class="row">
            <div class="col">
                <p>Test mess: {{ test_mess }}</p>
            </div>
        </div> -->
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Html5QrcodeScanner, Html5Qrcode } from "html5-qrcode";
import { useStore } from '@/store';
import BillDataService from "@/services/bills";
import { checkTokenExpired } from "@/http-common";

export default defineComponent({
    name: "qrscanner-page",
    data() {
        return {
            url_patterns: ["https://", "ic/", "mapr"] as Array<string>,
            status_messages: {
                1: this.$t("scanner.status.1"),
                2: this.$t("scanner.status.2"),
                3: this.$t("scanner.status.3")
            } as any,
            qrbox: 640 as number,
            percentage: 0.7 as number,
            fps: 10 as number,
            test_mess: "" as string,
            message: "" as string,
            found: false as boolean,
            html5QrcodeScanner: undefined as any,
            currentCameraID: "" as string,
            currentCameraName: "" as string,
            hasUserMedia: false as boolean,
            video: "" as any,
            src: "" as String,
            ctx: "" as any,
            canvas: "" as any,
            stream: "" as any,
            width: 240 as number,
            height: 240 as number,
            screenshotFormat: "image/jpeg" as string, 
            jpeg_quality: "" as string,
            picture: "" as string,
            result: {},
            windowHeight: window.innerHeight as number,
            windowWidth: window.innerWidth as number
        };
    },
    computed: {
      authToken() {
        const store = useStore();
        // console.log("store: ", store);
        return store.state.auth.token;
      },
      qrscannerStatusMessage(){
        let status = this.html5QrcodeScanner.getState();
        return this.status_messages[Number(status)];
      }
    },
    methods: {
        calculateSizes() {
            let factor = this.windowHeight/this.windowWidth;
            this.height = this.height * factor;
        },
        getCanvas() {
            // if (!this.hasUserMedia) return null;
            let video_ref: any = this.$refs;
            let video: any = null;
            if (video_ref) {
                video = video_ref[
                    "qr-scanner"
                ].children[1].children[0];
            }
            console.log("this.height: ", this.height);
            console.log("this.width: ", this.width);
            if (!this.ctx) {
                const canvas = document.createElement('canvas');
                canvas.height = this.height;
                canvas.width = this.width;
                this.canvas = canvas;
                this.ctx = canvas.getContext('2d');
            }
            this.ctx.drawImage(
                video, 
                - this.canvas.width/4, - this.canvas.height/4,
                this.canvas.width + this.canvas.width/4,
                this.canvas.height + this.canvas.height/4
            );
            return this.canvas;
        },
        getPhoto() {
            // if (!this.hasUserMedia) return null;
            const canvas = this.getCanvas();
            // console.log("this.jpeg_quality: ", this.jpeg_quality);
            return canvas.toDataURL(
                this.screenshotFormat, this.jpeg_quality
            );
        },
        async onScanSuccess(qrCodeMessage: string) {
            this.test_mess += qrCodeMessage;
            this.html5QrcodeScanner.pause();
            if (this.checkUrl(qrCodeMessage)){
                this.message = this.$t("scanner.message.correct_url");
            } else {
                this.message = this.$t("scanner.message.wrong_url");
            }
            this.found = true;
            await this.sendUrlToServer(qrCodeMessage);
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
                this.picture = this.getPhoto();
                // console.log(this.picture);
                let response = await BillDataService.sendUrl(
                    {"link": link, "image": this.picture},
                    this.authToken
                );
                this.message = this.$t("scanner.message.sent_to_server");
                this.html5QrcodeScanner.clear();
                this.$router.push({ 
                    name: "category_products_bill_id",
                    params: {bill_id: response.data.id}
                })
            } catch(e) {
                checkTokenExpired(e);
            }
        },
        qrboxFunction(
            viewfinderWidth: number,
            viewfinderHeight: number
        ) {
            let minEdgePercentage = this.percentage;
            let minEdgeSize = Math.min(
                viewfinderWidth, viewfinderHeight
            );
            let qrboxSize = Math.floor(
                minEdgeSize * minEdgePercentage
            );
            return {
                width: qrboxSize,
                height: qrboxSize
            }
        }
    },
    async mounted() {
        // this.calculateSizes();
        // let cameras = await Html5Qrcode.getCameras();
        // console.log("cameras: ", cameras);
        // for (let cam of cameras) {
        //     this.test_mess += cam.label + ", ";
        // }
        
        // for (let cam of cameras) {
        //     console.log("cam.name: ", cam.label);
        //     if (cam.label.includes("rear") || cam.label.includes("back")){
        //         this.currentCameraID = cam.id;
        //         this.currentCameraName = cam.label;
        //         console.log("choosen");
        //         console.log("cam.name: ", cam.label);
        //         console.log("cam.id: ", cam.id);
        //         break;
        //     } 
        // }
        // if (this.currentCameraID == ""){
        //     this.currentCameraID = cameras[0].id;
        //     this.currentCameraName = cameras[0].label;
        // }
        // console.log("this.currentCameraID: ", this.currentCameraID);
        let config = {
            fps: this.fps ? this.fps : 10,
            qrbox: this.qrboxFunction,
            // aspectRatio: 3 / 2,
            disableFlip: true
        };
        
        // this.html5QrcodeScanner = new Html5Qrcode("qr-scanner");
        // this.html5QrcodeScanner.start(
        //     this.currentCameraID, config,
        //     this.onScanSuccess  
        // );
        this.html5QrcodeScanner = new Html5QrcodeScanner(
            "qr-scanner", config, true
        );
        console.log("this.html5QrcodeScanner: ", this.html5QrcodeScanner)
        // this.html5QrcodeScanner.Html5QrcodeScannerStrings.scanButtonStartScanningText = () => {
        //     return this.$t("scanner.strings.start_scan");
        // }
        this.html5QrcodeScanner.render(
            this.onScanSuccess, undefined
        );
    }
})
</script>