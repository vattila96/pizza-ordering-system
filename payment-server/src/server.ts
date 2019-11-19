import * as http from 'http'
import * as dotenv from 'dotenv'
import app from './app'

dotenv.config()

const port = process.env.HTTP_PORT || 8080

const httpServer = http.createServer(app.callback())
//listen on provided port
httpServer.listen(port, (): void => {
  console.log(`Server is listening on port: ${port}`)
})
