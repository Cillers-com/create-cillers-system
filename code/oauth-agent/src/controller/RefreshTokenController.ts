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
import {
    decryptCookie, getAuthCookieName, getCookiesForTokenResponse, refreshAccessToken, validateIDtoken, ValidateRequestOptions
} from '../lib/index.js'
import {InvalidCookieException} from '../lib/exceptions/index.js'
import validateExpressRequest from '../validateExpressRequest.js'
import {asyncCatch} from '../middleware/exceptionMiddleware.js';

class RefreshTokenController {
    public router = express.Router()

    constructor() {
        this.router.post('/', asyncCatch(this.RefreshTokenFromCookie))
    }

    RefreshTokenFromCookie = async (req: express.Request, res: express.Response, next: express.NextFunction) => {

        // Check for an allowed origin and the presence of a CSRF token
        const options = new ValidateRequestOptions()
        validateExpressRequest(req, options)

        const authCookieName = getAuthCookieName(config.cookieNamePrefix)
        if (req.cookies && req.cookies[authCookieName]) {
            
            const refreshToken = decryptCookie(config.encKey, req.cookies[authCookieName])

            const tokenResponse = await refreshAccessToken(refreshToken, config)
            if (tokenResponse.id_token) {
                validateIDtoken(config, tokenResponse.id_token)
            }

            const cookiesToSet = getCookiesForTokenResponse(tokenResponse, config)
            res.setHeader('Set-Cookie', cookiesToSet)
            res.status(204).send()

        } else {
            const error = new InvalidCookieException()
            error.logInfo = 'No auth cookie was supplied in a token refresh call'
            throw error
        }
    }
}

export default RefreshTokenController
