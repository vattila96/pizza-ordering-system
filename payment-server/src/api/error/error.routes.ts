import Router from 'koa-router'
import { errorPage } from './error.controller'

const router: Router = new Router()

// @ts-ignore
router.get('/error', errorPage)

export default router
