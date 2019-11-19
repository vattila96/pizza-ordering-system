import { Context } from 'koa'
import { viewUrlHandler } from '../../utils/general-utils'

export const sayHello = async (ctx: Context): Promise<void> => {
  ctx.status = 200
  ctx.body = { message: 'Hello' }
}

export const sayHelloWithMustache = async (ctx: Context): Promise<void> => {
  await ctx.render(viewUrlHandler('payment/payment'))
}
