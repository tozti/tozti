const UglifyJsPlugin = require("uglifyjs-webpack-plugin")
const baseConfig = require('./base.config.js')
const merge = require('webpack-merge')

module.exports = merge(baseConfig, {
  plugins: [
    new UglifyJsPlugin({
      parallel: 8,
    })
  ]
})

