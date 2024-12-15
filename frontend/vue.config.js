const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = {
  configureWebpack: {
    plugins: [
      new MonacoWebpackPlugin({
        languages: ['javascript', 'python', 'sql'],
        features: ['!gotoSymbol']
      })
    ]
  }
} 