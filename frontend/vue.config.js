
const path = require('path');

module.exports = {
  devServer: {
    port: 5000
  },
  lintOnSave: false,
  runtimeCompiler: true,
  configureWebpack: {
    resolve: {
      alias: {
        components: path.resolve(__dirname, 'frontend/src/components/'),
        actions: path.resolve(__dirname, 'frontend/src/store/actions'),
        utils: path.resolve(__dirname, 'frontend/src/utils'),
        request: path.resolve(__dirname, 'frontend/src/request'),
      }
    }
  }
}
