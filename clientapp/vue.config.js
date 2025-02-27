const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
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

