import jwt
import logging
from typing import Optional

from . import env

logger = logging.getLogger(__name__)

#### Decoding ####

def decode_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token,
                          env.get_jwt_secret(),
                          algorithms=env.get_jwt_algorithms())
    except jwt.PyJWTError as e:
        logger.error(e)
        pass

