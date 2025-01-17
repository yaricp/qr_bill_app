<template>
    <main>
        
        <div v-if="html5QrcodeScanner" >
            <p>{{ qrscannerStatusMessage }}</p>
        </div>
        <div>
            <div ref="qr-scanner" id="qr-scanner"/>
        </div>
        <div><p>{{ message }}</p></div>
        <div><p>
            <img :src="picture" />
        </p></div>
        <div><p>Test mess: {{ test_mess }}</p></div>
        <div>{{currentCameraName}}</div>
    </main>
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
                1: "Choose camera for scanning",
                2: "Scan you bill with QR code",
                3: "Sending result to server"
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
                this.message = "Found Correct URL"
            } else {
                this.message = "Wrong URL!"
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
                this.message = "sent to server successful!"
                this.html5QrcodeScanner.clear();
                this.$router.push({ 
                    name: "category_goods_bill_id",
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
        let cameras = await Html5Qrcode.getCameras();
        console.log("cameras: ", cameras);
        for (let cam of cameras) {
            this.test_mess += cam.label + ", ";
        }
        for (let cam of cameras) {
            console.log("cam.name: ", cam.label);
            if (cam.label.includes("rear") || cam.label.includes("back")){
                this.currentCameraID = cam.id;
                this.currentCameraName = cam.label;
                console.log("choosen");
                console.log("cam.name: ", cam.label);
                console.log("cam.id: ", cam.id);
                break;
            } 
        }
        if (this.currentCameraID == ""){
            this.currentCameraID = cameras[0].id;
            this.currentCameraName = cameras[0].label;
        }
        console.log("this.currentCameraID: ", this.currentCameraID);
        let config = {
            fps: this.fps ? this.fps : 10,
            qrbox: this.qrboxFunction,
            // aspectRatio: 3 / 2,
            disableFlip: true
        };
        // this.html5QrcodeScanner = new Html5QrcodeScanner(
        //     "qr-scanner", config, true
        // );
        this.html5QrcodeScanner = new Html5Qrcode("qr-scanner");
        // this.html5QrcodeScanner.qrCodeSuccessCallback=this.onScanSuccess
        this.html5QrcodeScanner.start(
            this.currentCameraID, config,
            this.onScanSuccess  
        );
        // this.html5QrcodeScanner.render(
        //     this.onScanSuccess, undefined
        // );
    }
})
</script>