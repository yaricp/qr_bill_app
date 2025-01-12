const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    port: 8081
  },
  pwa: {
    name: 'My ToDo App',
    short_name: 'ToDo',
    description: 'A ToDo progressive web app',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#41b383',
    icons: [
      {
        src: '/img/icons/icon-72x72.png',
        sizes: '72x72',
        type: 'image/png',
      },
      // Add more icons for different resolutions as needed
    ],
  },
}