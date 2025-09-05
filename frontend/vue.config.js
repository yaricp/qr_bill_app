const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    port: 8081
  },
  pages: {
    index: {
      entry: "src/main.ts",
      title: "qr_bill_app.me"
    },
  },
  pwa: {
    workboxPluginMode: 'GenerateSW',
    manifestOptions: {
      name: "qr_bill_app",
      short_name: "qr_bill_app",
      icons: [
        {"src":"./img/icons/qr_bill_app-512.png","sizes":"512x512","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-384.png","sizes":"384x384","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-192.png","sizes":"192x192","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-152.png","sizes":"152x152","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-144.png","sizes":"144x144","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-128.png","sizes":"128x128","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-100.png","sizes":"100x100","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-96.png","sizes":"96x96","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-72.png","sizes":"72x72","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-48.png","sizes":"48x48","type":"image/png"},
        {"src":"./img/icons/qr_bill_app-32.png","sizes":"32x32","type":"image/png"}
      ],
      background_color: "#12b0db"
    }
  }
}
