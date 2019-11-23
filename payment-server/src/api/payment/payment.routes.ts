import Router from 'koa-router'
import { sayHello, processPayment } from './payment.controller'
import { assetServer } from '../asset-server'

const router: Router = new Router()

// @ts-ignore
router.get('/', sayHello)
// @ts-ignore
router.get('/process-payment', processPayment)
// @ts-ignore
router.get(/^(.+).css$/, assetServer)

export default router
