import env from '../../environment'

export const viewUrlHandler = (src: string): string => (env.isDev ?? false ? src : src.slice(-1))
