import dotenv from 'dotenv'
import { EnvironmentConfig } from 'environment.types'
dotenv.config()

const config: EnvironmentConfig = {
  isDev: process.env.ENVIRONMENT === 'development',
  requestLogging: process.env.REQUEST_LOGGING === 'enable',
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '27017', 10),
    dbName: process.env.DB_NAME || 'wave-db',
    username: process.env.MONGO_INITDB_ROOT_USERNAME || '',
    password: process.env.MONGO_INITDB_ROOT_PASSWORD || '',
    connectString: process.env.MONGODB_URI || '' // this overwrites everything above
  }
}

export default config
