import React, { useState, useEffect, useCallback } from 'react'
import { ApiClientRest } from '../../../rest/api_client_rest'
import { Item } from '../../../rest/modules/items'

interface ItemsProps {
    client: ApiClientRest
}

const Items: React.FC<ItemsProps> = ({ client }) => {
    const [items, setItems] = useState<Item[]>([])
    const [newItemText, setNewItemText] = useState('')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const handleError = useCallback((message: string, details?: any) => {
        console.error(`Error: ${message}`, details)
        setError(`${message}${details ? `: ${JSON.stringify(details)}` : ''}`)
    }, [])

    const fetchItems = useCallback(async () => {
        try {
            const response = await client.items.list()
            const data = response as Item[]
            console.log(data)
            setItems(data)
            setLoading(false)
        } catch (err) {
            handleError('Error fetching items', err)
            setLoading(false)
        }
    }, [client.items, handleError])

    useEffect(() => {
        fetchItems()
    }, [fetchItems])

    const handleAddItem = async () => {
        const name = newItemText.trim();
        setNewItemText('')
        if (!name) return
        try {
            const response = await client.items.create({ name: name })
            if ('id' in response) {
                setItems(prevItems => [...prevItems, {id: response.id, data: {name: name}}])
            } else {
                throw new Error('Unexpected response format when creating item')
            }
        } catch (err) {
            handleError('Error adding item', err)
        }
    }

    const handleRemoveItem = async (id: string) => {
        try {
            await client.items.remove(id)
            setItems(prevItems => prevItems.filter(item => item.id !== id))
        } catch (err) {
            handleError('Error removing item', err)
        }
    }

    if (loading)
        return (
            <div className="flex justify-center items-center min-h-screen bg-base-300">
                <button className="btn">
                    <span className="loading loading-spinner"></span>
                    Loading...
                </button>
            </div>
        )
    if (error) return <p className="text-error p-4">{'Error: ' + error}</p>

    return (
        <div className="min-h-screen flex flex-col">
            <div className="navbar bg-base-300 text-neutral-content">
                <div className="flex-1">
                    <a href="/" className="p-2 normal-case text-xl">
                        REST API Demo
                    </a>
                </div>
            </div>

            <div className="flex flex-grow justify-center items-center bg-neutral">
                <div className="card card-compact w-full max-w-lg bg-base-100 shadow-xl">
                    <div className="card-body items-stretch text-center">
                        <h1 className="card-title self-center text-2xl font-bold mb-4">
                            Item List
                        </h1>
                        <div className="form-control w-full">
                            <div className="join">
                                <input
                                    type="text"
                                    placeholder="Add new item..."
                                    className="join-item flex-grow input input-bordered input-md input-primary"
                                    value={newItemText}
                                    onChange={(e) => setNewItemText(e.target.value)}
                                />
                                <button
                                    className="join-item btn btn-square btn-md btn-primary"
                                    onClick={handleAddItem}
                                >
                                    Add
                                </button>
                            </div>
                        </div>
                        <div className="space-y-2 w-full">
                            {items.map(({ data, id }: Item) => (
                                <div
                                    key={id}
                                    className="card card-compact w-full bg-base-200 flex-row items-center justify-between"
                                >
                                    <div className="card-body">
                                        <div className="flex justify-between items-center w-full">
                                            <span>{data.name}</span>
                                            <button
                                                className="btn btn-xs btn-circle btn-error"
                                                onClick={() => handleRemoveItem(id)}
                                            >
                                                x
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Items
