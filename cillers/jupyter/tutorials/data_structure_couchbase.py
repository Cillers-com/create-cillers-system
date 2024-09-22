from couchbase.exceptions import ScopeAlreadyExistsException, CollectionAlreadyExistsException
from couchbase.management.collections import CreateCollectionSettings

def create_scope(collection_manager, scope_name):
    try:
        collection_manager.create_scope(scope_name)
        print(f"Scope '{scope_name}' created successfully.")
    except ScopeAlreadyExistsException:
        print(f"Scope '{scope_name}' already exists.")
    except Exception as e:
        print(f"An error occurred while creating scope: {e}")

def create_collections(collection_manager, scope_name, collection_names):
    for collection_name in collection_names:
        try:
            collection_manager.create_collection(
                scope_name,
                collection_name,
                CreateCollectionSettings()
            )
            print(f"Collection '{collection_name}' created successfully in scope '{scope_name}'.")
        except CollectionAlreadyExistsException:
            print(f"Collection '{collection_name}' already exists in scope '{scope_name}'.")
        except Exception as e:
            print(f"An error occurred while creating collection '{collection_name}': {e}")

def create(bucket, spec):
    collection_manager = bucket.collections()
    for scope_name, collection_names in spec.items():
        create_scope(collection_manager, scope_name)
        create_collections(collection_manager, scope_name, collection_names) 