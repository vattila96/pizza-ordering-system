import './payment.scss'
import { StringIndexable } from '../../types'

const successButton = document.getElementById('success-button')
const failureButton = document.getElementById('failure-button')

enum REDIRECT_STATUS {
  SUCCESS = 'success',
  FAILURE = 'failure'
}

//localhost:9000/process-payment?redirect=http://localhost:8000&amount=18000
const getUrlParam = (name: string): string | null => {
  // this is not my most robust function ever
  const url = window.location.href
  if (url.indexOf('?') === -1) return null

  type ParamStorage = StringIndexable<string>

  const magic: ParamStorage = url
    .split('?')[1]
    .split('&')
    .reduce((a: ParamStorage, c: string): ParamStorage => {
      const [name, val] = c.split('=')
      return { ...a, [name]: val }
    }, {} as ParamStorage)

  return magic[name] ?? null
}

const cleanUriEnding = (uri: string): string => (uri.charAt(uri.length) === '/' ? uri.slice(0, -1) : uri)

const redirectWithStatus = (status: REDIRECT_STATUS): void => {
  let redirectUri = ''
  try {
    redirectUri = cleanUriEnding(getUrlParam('redirect') ?? '/')
  } catch (e) {
    console.error('Unable to determine redirect uri!')
    console.error(e.toString())
    return
  }

  window.location.href = redirectUri.concat(`?status=${status}`)
}

successButton?.addEventListener('click', (e: MouseEvent): void => {
  e.preventDefault()
  redirectWithStatus(REDIRECT_STATUS.SUCCESS)
})

failureButton?.addEventListener('click', (e: MouseEvent) => {
  e.preventDefault()
  redirectWithStatus(REDIRECT_STATUS.FAILURE)
})
