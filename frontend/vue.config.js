const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    port: 8081
  },
  pwa: {
    workboxPluginMode: 'GenerateSW',
    manifestOptions: {
      name: "QRacun",
      short_name: "QRacun",
      icons: [
        {"src":"./img/icons/qracun-512.png","sizes":"512x512","type":"image/png"},
        {"src":"./img/icons/qracun-384.png","sizes":"384x384","type":"image/png"},
        {"src":"./img/icons/qracun-192.png","sizes":"192x192","type":"image/png"},
        {"src":"./img/icons/qracun-152.png","sizes":"152x152","type":"image/png"},
        {"src":"./img/icons/qracun-144.png","sizes":"144x144","type":"image/png"},
        {"src":"./img/icons/qracun-128.png","sizes":"128x128","type":"image/png"},
        {"src":"./img/icons/qracun-100.png","sizes":"100x100","type":"image/png"},
        {"src":"./img/icons/qracun-96.png","sizes":"96x96","type":"image/png"},
        {"src":"./img/icons/qracun-72.png","sizes":"72x72","type":"image/png"},
        {"src":"./img/icons/qracun-48.png","sizes":"48x48","type":"image/png"},
        {"src":"./img/icons/qracun-32.png","sizes":"32x32","type":"image/png"}
      ],
      background_color: "#12b0db"
    }
  }
}
