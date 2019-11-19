export interface EnvironmentConfig {
  isDev: boolean
  database: {
    host: string
    port: number
    dbName: string
    username: string
    password: string
    connectString: string
  }
}
