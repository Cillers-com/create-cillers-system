import React, { useMemo } from 'react'
import {ApiClientRest} from '../../../rest/api_client_rest'
import Items from './Items'

const Demo: React.FC = () => {
    const client = useMemo(() => new ApiClientRest(), [])

    return (
        <div>
            <Items client={client} />
        </div>
    )
}

export default Demo
