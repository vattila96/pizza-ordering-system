import env from '../../environment'

export const viewUrlHandler = (src: string): string =>
  // eslint-disable-next-line prettier/prettier
  (env.isDev ?? false) ? src : src.split('/').slice(-1).join('')
