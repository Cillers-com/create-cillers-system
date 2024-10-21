import React, { useState, useEffect, useCallback } from 'react'
import { ApiClientRest } from '../../../rest/api_client_rest'
import { Item } from '../../../rest/modules/items'

interface ItemsProps {
    client: ApiClientRest
}

interface ApiResponse {
    items: Item[]
}

const Items: React.FC<ItemsProps> = ({ client }) => {
    const [items, setItems] = useState<Item[]>([])
    const [newItemText, setNewItemText] = useState('')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const fetchItems = useCallback(async () => {
        try {
            const response = await client.items.list()
            
            if (typeof response === 'object' && response !== null && 'items' in response) {
                const data = response as ApiResponse
                setItems(data.items)
            } else {
                throw new Error('Unexpected response format')
            }
            setLoading(false)
        } catch (err) {
            setError('Error fetching items: ' + (err instanceof Error ? err.message : String(err)))
            setLoading(false)
        }
    }, [client.items])

    useEffect(() => {
        fetchItems()
    }, [fetchItems])

    const handleAddItem = async () => {
        if (!newItemText.trim()) return
        try {
            const response = await client.items.create([{ name: newItemText }])
            if (typeof response === 'object' && response !== null && 'items' in response) {
                const data = response as ApiResponse
                setItems(prevItems => [...prevItems, ...data.items])
                setNewItemText('')
            } else {
                throw new Error('Unexpected response format when creating item')
            }
        } catch (err) {
            setError('Error adding item: ' + (err instanceof Error ? err.message : String(err)))
        }
    }

    const handleRemoveItem = async (id: string) => {
        try {
            await client.items.remove(id)
            setItems(prevItems => prevItems.filter(item => item.id !== id))
        } catch (err) {
            setError('Error removing item: ' + (err instanceof Error ? err.message : String(err)))
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
                            {items.map(({ name, id }: Item) => (
                                <div
                                    key={id}
                                    className="card card-compact w-full bg-base-200 flex-row items-center justify-between"
                                >
                                    <div className="card-body">
                                        <div className="flex justify-between items-center w-full">
                                            <span>{name}</span>
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
