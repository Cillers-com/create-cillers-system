import uuid
import strawberry
from . import couchbase as cb, env

@strawberry.type
class Product:
    id: str
    name: str
    
@strawberry.type
class Game:
    name: str
    host: str
    
def create_product(name: str) -> Product:
    id = str(uuid.uuid1())
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='products',
                         key=id,
                         data={'name': name}))
    return Product(id=id, name=name)
#
def get_product(id: str) -> Product | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='products',
                               key=id)):
        return Product(id=id, name=doc['name'])

def delete_product(id: str) -> None:
    cb.remove(env.get_couchbase_conf(),
              cb.DocRef(bucket=env.get_couchbase_bucket(),
                        collection='products',
                        key=id))

def list_products() -> list[Product]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.products"
    )
    return [Product(**r) for r in result]

def create_game(name: str, host: str) -> Game:
    cb.insert(
        env.get_couchbase_conf(),
        cb.DocSpec(
            bucket=env.get_couchbase_bucket(),
            collection='games',
            key=name,
            data={
                'name': name,
                'host': host,
            }
        )
    )
    
    return Game(name=name, host=host)

def add_player(game_name: str, name: str) -> bool:
    # Check that game exists.
    try:
        cb.get(
            env.get_couchbase_conf(),
            cb.DocRef(
                key=game_name,
                bucket=env.get_couchbase_bucket(),
                collection='games',   
            )
        )
    except:
        return False
    
    cb.insert(
        env.get_couchbase_conf(),
        cb.DocSpec(
            bucket=env.get_couchbase_bucket(),
            collection='players',
            key=game_name+name,
            data={
                'name': name,
                'game_name': game_name,
            }
        )
    )
    
    return True

def list_players(game_name: str) -> list[str]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name FROM {env.get_couchbase_bucket()}._default.players WHERE game_name = '{game_name}'"
    )
    
    return [r['name'] for r in result]