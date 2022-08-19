from msio.logme.domain.entities import Token, User
from msio.logme.domain.repositories import TokenRepository


class ThreadMemoryTokenRepository(TokenRepository):
    def __init__(self, cache):
        self.cache = cache

    async def has_token(self, token: Token) -> bool:
        return self.cache.get(token.value, None) is not None

    async def save_token(self, token: Token) -> None:
        self.cache[token.value] = token.user_id

    async def forget_token(self, token: Token) -> None:
        self.cache.pop(token.value, None)
