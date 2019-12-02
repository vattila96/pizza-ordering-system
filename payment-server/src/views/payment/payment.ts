import './payment.scss'

const successButton = document.getElementById('success-button')
const failureButton = document.getElementById('failure-button')

enum REDIRECT_STATUS {
  SUCCESS = 'success',
  FAILURE = 'failure'
}

const determineRedirectUri = (): string => window.location.href.split('=')[1]

const redirectWithStatus = (status: REDIRECT_STATUS): void => {
  let redirectUri = ''
  try {
    redirectUri = determineRedirectUri()
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
