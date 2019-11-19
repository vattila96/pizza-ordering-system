import Koa from 'koa'
import bodyParser from 'koa-bodyparser'
import render from 'koa-ejs'
import mainRouter from './api/payment/payment.routes'
import envConfig from '../environment'

const { isDev } = envConfig

const app: Koa = new Koa()

app
  .use(bodyParser())
  .use(mainRouter.middleware())
  .use(mainRouter.allowedMethods())

// @ts-ignore
render(app, {
  root: isDev ? './src/views' : './dist',
  layout: false,
  viewExt: 'ejs',
  cache: !isDev,
  debug: isDev
})

export default app
