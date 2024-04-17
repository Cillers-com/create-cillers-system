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

import express from 'express'
import {config} from '../config.js'
import {getATCookieName, getCookiesForUnset, getLogoutURL, ValidateRequestOptions} from '../lib/index.js'
import {InvalidCookieException} from '../lib/exceptions/index.js'
import validateExpressRequest from '../validateExpressRequest.js'
import {asyncCatch} from '../middleware/exceptionMiddleware.js';

class LogoutController {
    public router = express.Router()

    constructor() {
        this.router.post('/', asyncCatch(this.logoutUser))
    }

    logoutUser = async (req: express.Request, res: express.Response, next: express.NextFunction) => {

        // Check for an allowed origin and the presence of a CSRF token
        const options = new ValidateRequestOptions()
        validateExpressRequest(req, options)

        if (req.cookies && req.cookies[getATCookieName(config.cookieNamePrefix)]) {

            const logoutURL = getLogoutURL(config)
            res.setHeader('Set-Cookie', getCookiesForUnset(config.cookieOptions, config.cookieNamePrefix))
            res.json({ url: logoutURL})

        } else {
            const error = new InvalidCookieException()
            error.logInfo = 'No auth cookie was supplied in a logout call'
            throw error
        }
    }
}

export default LogoutController
