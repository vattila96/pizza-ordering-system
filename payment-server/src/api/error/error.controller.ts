import { Context } from 'koa'
import { viewUrlHandler } from '../../utils/general-utils'

export const errorPage = async (ctx: Context): Promise<void> => {
  const errors = [
    { code: 400, description: 'Bad request. A szerverhez intézett kérés hibás volt, vagy rossz formátumú.' },
    { code: 500, description: 'Internal server error. Belső hiba történt.' }
  ]

  await ctx.render(viewUrlHandler('error/error'), {
    description: errors.find(({ code }) => String(code) === ctx.query.code)?.description ?? ''
  })
}
