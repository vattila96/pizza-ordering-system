import { Context } from 'koa'
import fs from 'fs'
import path from 'path'

export const assetServer = async (ctx: Context): Promise<void> => {
  const contentTypes = [
    { ext: 'css', ct: 'text/css' },
    { ext: 'js', ct: 'text/javascript' }
  ]
  const assetPath = path.resolve(process.cwd(), 'dist', ctx.path.slice(1))
  let ext = ''
  try {
    ext = ctx.path
      .split('/')
      .slice(-1)[0]
      .split('.')
      .slice(-1)[0]
  } catch (e) {
    console.error('could not determine asset extension!')
    console.info({ request: ctx.path })
    ctx.status = 400
    ctx.body = { message: 'could not determine asset extension!' }
    return
  }

  try {
    if (!fs.existsSync(assetPath)) {
      ctx.status = 404
      ctx.message = 'Not Found'
      console.info('Could not serve asset, because it does not exists: ', { path: assetPath })
      return
    }

    ctx.status = 200
    ctx.set('Content-Type', contentTypes.find(({ ext: e }) => ext === e)?.ct ?? 'text/plain')
    ctx.body = fs.readFileSync(assetPath, { encoding: 'UTF-8', flag: 'r' })
  } catch (e) {
    console.error('could not serve asset:', assetPath)
    console.error(e.toString())
    ctx.status = 500
  }
}
