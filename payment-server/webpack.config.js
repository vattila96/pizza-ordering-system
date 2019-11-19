/* eslint-disable @typescript-eslint/no-var-requires,@typescript-eslint/explicit-function-return-type */
const fs = require('fs')
const path = require('path')
const NodemonPlugin = require('nodemon-webpack-plugin')
const CopyPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

const isDev = process.env.ENVIRONMENT === 'development'

const nodeModules = fs
  .readdirSync('node_modules')
  .reduce((acc, dir) => (dir === '.bin' ? acc : { ...acc, [dir]: `commonjs ${dir}` }), {})

module.exports = {
  entry: {
    server: './src/server.ts',
    payment: './src/views/payment/payment.ts'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist')
  },
  target: 'node',
  module: {
    rules: [
      { test: /\.ts$/, loader: 'ts-loader' },
      {
        test: /\.scss$/,
        use: [
          { loader: MiniCssExtractPlugin.loader },
          { loader: 'css-loader' },
          { loader: 'postcss-loader' },
          {
            loader: 'sass-loader',
            options: { sourceMap: true }
          }
        ]
      },
      {
        test: /\.ejs$/,
        loader: 'ejs-loader',
        options: {
          variable: 'data',
          interpolate: '\\{\\{(.+?)\\}\\}',
          evaluate: '\\[\\[(.+?)\\]\\]'
        }
      }
    ]
  },
  externals: nodeModules,
  watch: isDev,
  mode: isDev ? 'development' : 'production',
  watchOptions: { ignored: /nodeModules/ },
  resolve: { extensions: ['.ts', '.js', '.scss', '.ejs'] },
  plugins: [
    new NodemonPlugin({
      script: './dist/server.js',
      watch: path.resolve('./dist')
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
      ignoreOrder: false // Enable to remove warnings about conflicting order
    }),
    new CopyPlugin([
      {
        from: './src/views/**/*.ejs',
        flatten: true
      }
    ])
  ]
}
