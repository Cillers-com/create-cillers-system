import React, { useState, useEffect, useCallback } from 'react'
import { ApiClientRest } from '../../../rest/api_client_rest'
import { Item } from '../../../rest/modules/items'

interface ItemsProps {
    client: ApiClientRest
}

const Items: React.FC<ItemsProps> = ({ client }) => {
    const [items, setItems] = useState<Item[]>([])
    const [new_item_text, set_new_item_text] = useState('')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const fetch_items = useCallback(async () => {
        try {
            const data = await client.items.list()
            setItems(data)
            setLoading(false)
        } catch (err) {
            setError('Error fetching items')
            setLoading(false)
        }
    }, [client.items])

    useEffect(() => {
        fetch_items()
    }, [fetch_items])

    const handle_add_item = async () => {
        if (!new_item_text.trim()) return
        try {
            const new_items = await client.items.create([{ name: new_item_text }])
            if (new_items && new_items.length > 0) {
                setItems([...items, ...new_items])
                set_new_item_text('')
            }
        } catch (err) {
            setError('Error adding item')
        }
    }

    const handle_remove_item = async (id: string) => {
        try {
            await client.items.remove(id)
            setItems(items.filter(item => item.id !== id))
        } catch (err) {
            setError('Error removing item')
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
    if (error) return <p>{'Error: ' + error}</p>

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
                                    value={new_item_text}
                                    onChange={(e) => set_new_item_text(e.target.value)}
                                />
                                <button
                                    className="join-item btn btn-square btn-md btn-primary"
                                    onClick={handle_add_item}
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
                                                onClick={() => handle_remove_item(id)}
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
