/*
 *  Copyright 2021 Curity AB
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

import * as express from 'express'
import * as cors from 'cors'
import * as cookieParser from 'cookie-parser'
import * as fs from 'fs'
import * as https from 'https'
import {
    LoginController,
    UserInfoController,
    ClaimsController,
    LogoutController,
    RefreshTokenController
} from './controller'
import {config} from './config'
import loggingMiddleware from './middleware/loggingMiddleware'
import exceptionMiddleware from './middleware/exceptionMiddleware'

const app = express()
const corsConfiguration = {
    origin: config.trustedWebOrigins,
    credentials: true,
    methods: ['POST']
}

if (config.corsEnabled) {
    app.use(cors(corsConfiguration))
}

app.use(cookieParser())
app.use('*', express.json())
app.use('*', loggingMiddleware)
app.use('*', exceptionMiddleware)
app.set('etag', false)

const controllers = {
    '/login': new LoginController(),
    '/userInfo': new UserInfoController(),
    '/claims': new ClaimsController(),
    '/logout': new LogoutController(),
    '/refresh': new RefreshTokenController()
}

for (const [path, controller] of Object.entries(controllers)) {
    app.use(config.endpointsPrefix + path, controller.router)
}

if (config.serverCertPath) {

    const pfx = fs.readFileSync(config.serverCertPath);
    const sslOptions = {
        pfx,
        passphrase: config.serverCertPassword,
    };

    const httpsServer = https.createServer(sslOptions, app);
    httpsServer.listen(config.port, () => {
        console.log(`OAuth Agent is listening on HTTPS port ${config.port}`);
    });

} else {

    app.listen(config.port, function() {
        console.log(`OAuth Agent is listening on HTTP port ${config.port}`)
    })
}