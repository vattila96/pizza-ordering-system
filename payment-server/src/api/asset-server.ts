import fs from 'fs'
import { Context } from 'koa'

import envConfig from '../../environment'
const { isDev } = envConfig

export const assetServer = async (ctx: Context): Promise<void> => {
  const cssPath = `${isDev ? './dist/' : ''}${ctx.path.slice(1)}`
  try {
    if (!fs.existsSync(cssPath)) {
      ctx.status = 404
      ctx.message = 'Not Found'
      console.info('Could not serve asset, because it does not exists: ', { path: cssPath })
      return
    }

    ctx.status = 200
    ctx.set('Content-Type', 'text/css')
    ctx.body = await fs.readFileSync(`./${cssPath}`, { encoding: 'UTF-8', flag: 'r' })
  } catch (e) {
    console.error('could not serve asset:', cssPath)
    console.error(e.toString())
    ctx.status = 500
  }
}
