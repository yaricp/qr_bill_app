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
      name: "MyApp",
      short_name: "MyApp",
    }
  }
}
