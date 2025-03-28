const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',  // Ensure the server is accessible from outside the container
    port: process.env.VUE_APP_VUE_PORT,
    proxy: {
      "/api": {
        target: "http://api:8000", 
        changeOrigin: true,
        pathRewrite: { 
          "^/api": "/api"  // Keep the /api in the request path
        },
      },
    },
  },
});

