import React, { useState } from 'react';
import { useMutation, useSubscription } from '@apollo/client';
import { ITEMS_CREATE, ITEMS_REMOVE, ITEMS_SUBSCRIPTION } from '../graphql/items';

interface Item {
    id: string;
    name: string;
}

const Items: React.FC = () => {
    const [newItemName, setNewItemName] = useState('');
    const [items, setItems] = useState<Item[]>([]);
    const [addItems] = useMutation(ITEMS_CREATE, { errorPolicy: "all" });
    const [removeItem] = useMutation(ITEMS_REMOVE);
    
    const {loading, error} = useSubscription(ITEMS_SUBSCRIPTION, {
        onData: ({data}) => {
            if (data.data.items.existing) {
                setItems((prev) => prev.concat(...filterDuplicateItems(data.data.items.existing)))
            }
            if (data.data.items.created) {
                setItems((prev) => prev.concat(...filterDuplicateItems(data.data.items.created)))
            }
        }
    });

    const filterDuplicateItems = (receivedNewItems: Item[]) => {
        return receivedNewItems.filter((newItem: Item) => {
            return !items.some((item: Item) => item.id === newItem.id)
        })
    }

    const handleAddItem = async () => {
        if (!newItemName.trim()) return;
        await addItems({variables: {items: [{name: newItemName}]}});
        setNewItemName('');
    };

    const handleRemoveItem = async (id: string) => {
        setItems(items.filter((item) => item.id !== id))
        await removeItem({
            variables: {ids: [id]},
        });
    };

    if (error) {
        console.error("Subscription error:", error);
        return <p>Error in subscription</p>;
    }

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen bg-base-300">
                <button className="btn">
                    <span className="loading loading-spinner"></span>
                    Loading...
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex flex-col">
            <div className="navbar bg-base-300 text-neutral-content">
                <div className="flex-1">
                    <a href="/" className="p-2 normal-case text-xl">Items</a>
                </div>
            </div>

            <div className="flex flex-grow justify-center items-center bg-neutral">
                <div className="card card-compact w-full max-w-lg bg-base-100 shadow-xl">
                    <div className="card-body items-stretch text-center">
                        <h1 className="card-title self-center text-2xl font-bold mb-4">Item List</h1>
                        <div className="form-control w-full">
                            <div className="join">
                                <input
                                    type="text"
                                    placeholder="Add new item..."
                                    className="join-item flex-grow input input-bordered input-md input-primary"
                                    value={newItemName}
                                    onChange={(e) => setNewItemName(e.target.value)}
                                />
                                <button className="join-item btn btn-square btn-md btn-primary" onClick={handleAddItem}>
                                    Add
                              </button>
                          </div>
                      </div>
                      <div className="space-y-2 w-full">
                          {items.map(({name, id}: Item) => (
                              <div key={id} className="card card-compact w-full bg-base-200 flex-row items-center justify-between">
                                  <div className="card-body">
                                      <div className="flex justify-between items-center w-full">
                                          <span>{name}</span>
                                          <button className="btn btn-xs btn-circle btn-error" onClick={() => handleRemoveItem(id)}>
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
    );
};

export default Items;
