import Router from 'koa-router'
import { sayHello, sayHelloWithMustache } from './payment.controller'
import { assetServer } from '../asset-server'

const router: Router = new Router()

// @ts-ignore
router.get('/', sayHelloWithMustache)
// @ts-ignore
router.get('/hello-lean', sayHello)
// @ts-ignore
router.get(/^(.+).css$/, assetServer)

export default router
