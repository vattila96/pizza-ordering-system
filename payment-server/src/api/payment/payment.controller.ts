import { Context } from 'koa'
import { viewUrlHandler } from '../../utils/general-utils'

export const sayHello = async (ctx: Context): Promise<void> => {
  ctx.status = 200
  ctx.body = { message: 'use: /process-payment?redirect=<your redirect target here>' }
}

export const processPayment = async (ctx: Context): Promise<void> => {
  const redirectUri = ctx.query.redirect
  if (!redirectUri) ctx.redirect('/error?code=400')
  await ctx.render(viewUrlHandler('payment/payment'))
}
