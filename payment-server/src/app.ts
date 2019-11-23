import Koa, { Context, Next } from 'koa'
import bodyParser from 'koa-bodyparser'
import render from 'koa-ejs'
import mainRouter from './api/payment/payment.routes'
import errorRouter from './api/error/error.routes'
import envConfig from '../environment'

const { isDev, requestLogging } = envConfig

const app: Koa = new Koa()

app
  .use(bodyParser())
  .use(async (context: Context, next: Next) => {
    if (!requestLogging) return next()
    const start = Date.now()
    await next()
    const { method, path } = context
    console.info({ method, path, duration: `${Date.now() - start} ms` })
  })
  .use(mainRouter.middleware())
  .use(mainRouter.allowedMethods())
  .use(errorRouter.middleware())
  .use(errorRouter.allowedMethods())

// @ts-ignore
render(app, {
  root: isDev ? './src/views' : './dist',
  layout: false,
  viewExt: 'ejs',
  cache: !isDev,
  debug: isDev
})

export default app
