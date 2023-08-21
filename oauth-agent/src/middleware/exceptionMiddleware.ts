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

import {NextFunction, Request, Response} from 'express';
import {config} from '../config'
import {getCookiesForUnset } from'../lib';
import {OAuthAgentException} from '../lib/exceptions'
import {UnhandledException} from '../lib/exceptions'
import {RequestLog} from './requestLog';

export default function exceptionMiddleware(
    caught: any,
    request: Request,
    response: Response,
    next: NextFunction): void {

    const exception = caught instanceof OAuthAgentException ? caught : new UnhandledException(caught)
    
    if (!response.locals.log) {
        
        // For malformed JSON errors, middleware does not get created so write the whole log here
        response.locals.log = new RequestLog()
        response.locals.log.start(request)
        response.locals.log.addError(exception)
        response.locals.log.end(response)

    } else {

        // Otherwise just include error details in logs
        response.locals.log.addError(exception)
    }
    
    const statusCode = exception.statusCode
    const data = { code: exception.code, message: exception.message}
    
    // Send the error response to the client and remove cookies when the session expires
    response.status(statusCode)
    if (data.code === 'session_expired') {
        response.setHeader('Set-Cookie', getCookiesForUnset(config.cookieOptions, config.cookieNamePrefix))
    }
    response.send(data)
}

/*
 * Unhandled promise rejections may not be caught properly
 * https://medium.com/@Abazhenov/using-async-await-in-express-with-node-8-b8af872c0016
 */
export function asyncCatch(fn: any): any {

    return (request: Request, response: Response, next: NextFunction) => {

        Promise
            .resolve(fn(request, response, next))
            .catch((e) => {
                exceptionMiddleware(e, request, response, next)
            })
    };
}