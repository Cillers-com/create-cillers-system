import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { GET_PRODUCTS, ADD_PRODUCT, REMOVE_PRODUCT, PRODUCT_ADDED_SUBSCRIPTION } from '../graphql/operations';

interface Product {
  id: string;
  name: string;
}

interface GetProductsQuery {
  products: Product[];
}

const Products: React.FC = () => {
  const [newProductText, setNewProductText] = useState('');
  const [pushToKafka, setPushToKafka] = useState(false);
  const { data, loading, error, subscribeToMore } = useQuery(GET_PRODUCTS);
  const [addProduct] = useMutation(ADD_PRODUCT);
  const [removeProduct] = useMutation(REMOVE_PRODUCT);

  useEffect(() => {
    subscribeToMore({
      document: PRODUCT_ADDED_SUBSCRIPTION,
      updateQuery: (prev, { subscriptionData }) => {
        if (!subscriptionData.data) return prev;
        const newProduct = subscriptionData.data.productAdded;

        if (prev.products.some((product: Product) => product.id === newProduct.id)) {
          return prev;
        }
        return Object.assign({}, prev, {
          products: [...prev.products, newProduct]
        });
      },
    });
  }, [subscribeToMore]);

  if (loading) return (
    <div className="flex justify-center items-center min-h-screen bg-base-300">
      <button className="btn">
        <span className="loading loading-spinner"></span>
        Loading...
      </button>
    </div>
  );
  if (error) return <p>{'Error: ' + error}</p>;

  const handleAddProduct = async () => {
    if (!newProductText.trim()) return;
    if (pushToKafka) {
      const response = await fetch('/input/add_product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newProductText }),
      });
      if (response.ok) {
        setNewProductText('');
      } else {
        const errorText = await response.text();
        console.error('Failed to add product:', errorText);
      }
    } else {
      await addProduct({ variables: { name: newProductText } });
      setNewProductText('');
    }
  };

  const handleRemoveProduct = async (id: string) => {
    await removeProduct({
      variables: { id },
      update(cache) {
        const existingProducts = cache.readQuery<GetProductsQuery>({ query: GET_PRODUCTS });
        if (existingProducts?.products) {
          cache.writeQuery({
            query: GET_PRODUCTS,
            data: {
              products: existingProducts.products.filter(product => product.id !== id),
            },
          });
        }
      },
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <div className="navbar bg-base-300 text-neutral-content">
        <div className="flex-1">
          <a href="/" className="p-2 normal-case text-xl">Products</a>
        </div>
      </div>

      <div className="flex flex-grow justify-center items-center bg-neutral">
        <div className="card card-compact w-full max-w-lg bg-base-100 shadow-xl">
          <div className="card-body items-stretch text-center">
            <h1 className="card-title self-center text-2xl font-bold mb-4">Product List</h1>
            <div className="form-control w-full">
              <div className="join">
                <input
                  type="text"
                  placeholder="Add new product..."
                  className="join-item flex-grow input input-bordered input-md input-primary"
                  value={newProductText}
                  onChange={(e) => setNewProductText(e.target.value)}
                />
                <button className="join-item btn btn-square btn-md btn-primary" onClick={handleAddProduct}>
                  Add
                </button>
              </div>
            </div>
            <div className="space-y-2 w-full">
              {data.products.map(({ name, id }: Product) => (
                <div key={id} className="card card-compact w-full bg-base-200 flex-row items-center justify-between">
                  <div className="card-body">
                    <div className="flex justify-between items-center w-full">
                      <span>{name}</span>
                      <button className="btn btn-xs btn-circle btn-error" onClick={() => handleRemoveProduct(id)}>
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

export default Products;
