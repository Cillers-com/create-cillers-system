import React, { useMemo } from 'react'
import {ApiClientRest} from '../../../rest/api_client_rest'
import Items from './Items'

interface DemoProps {
    csrf: string
}

const Demo: React.FC<DemoProps> = ({ csrf }) => {
    const client = useMemo(() => new ApiClientRest(csrf), [csrf])

    return (
        <div>
            <Items client={client} />
        </div>
    )
}

export default Demo
