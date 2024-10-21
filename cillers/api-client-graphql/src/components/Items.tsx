import React, { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@apollo/client'
import {
  ITEMS,
  ITEMS_CREATE,
  ITEMS_REMOVE,
  ITEMS_CREATED,
} from '../graphql/items'

interface Item {
  id: string
  name: string
}

interface GetItemsQuery {
  items: Item[]
}

const Items: React.FC = () => {
  const [newItemText, setNewItemText] = useState('')
  const { data, loading, error, subscribeToMore } = useQuery(ITEMS)
  const [addItem] = useMutation(ITEMS_CREATE, { errorPolicy: 'all' })
  const [removeItem] = useMutation(ITEMS_REMOVE)

  useEffect(() => {
    subscribeToMore({
      document: ITEMS_CREATED,
      updateQuery: (prev, { subscriptionData }) => {
        if (!subscriptionData.data) return prev
        const newItem = subscriptionData.data.itemsCreated

        if (prev.items.some((item: Item) => item.id === newItem.id)) {
          return prev
        }
        return Object.assign({}, prev, {
          items: [...prev.items, newItem],
        })
      },
    })
  }, [subscribeToMore])

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

  const handleAddItem = async () => {
    if (!newItemText.trim()) return
    await addItem({ variables: { items: [{ name: newItemText }] } })
    setNewItemText('')
  }

  const handleRemoveItem = async (id: string) => {
    await removeItem({
      variables: { ids: [id] },
      update(cache) {
        const existingItems = cache.readQuery<GetItemsQuery>({ query: ITEMS })
        if (existingItems?.items) {
          cache.writeQuery({
            query: ITEMS,
            data: {
              items: existingItems.items.filter((item) => item.id !== id),
            },
          })
        }
      },
    })
  }

  return (
    <div className="min-h-screen flex flex-col">
      <div className="navbar bg-base-300 text-neutral-content">
        <div className="flex-1">
          <a href="/" className="p-2 normal-case text-xl">
            Items
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
              {data.items.map(({ name, id }: Item) => (
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
