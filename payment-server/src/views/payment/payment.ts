import './payment.scss'

const successButton = document.getElementById('success-button')
const failureButton = document.getElementById('failure-button')

successButton?.addEventListener('click', (e: MouseEvent): void => {
  e.preventDefault()
  // todo: change this ordenáré solution
  const redirectUri = successButton.getAttribute('data-redirect')
  if (!redirectUri) return

  window.location.href = redirectUri
})
