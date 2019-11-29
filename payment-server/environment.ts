import dotenv from 'dotenv'
import { EnvironmentConfig } from 'environment.types'
dotenv.config()

const config: EnvironmentConfig = {
  isDev: process.env.ENVIRONMENT === 'development',
  requestLogging: process.env.REQUEST_LOGGING === 'enable'
}

export default config
