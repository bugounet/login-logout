from msio.logme.domain.entities import Token
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

    async def forget_user(self, user_id: int) -> None:
        # bad implementation choice discovered: this algorithm is
        # not efficient. We should keep tests on the interface
        # and refactor implementation since it won't scale well...
        #
        # OR we could implement a new interface, and swap it progressively
        # on a lower percentage of input requests so that we can deploy
        # it with fewer risks... \o/
        tokens_to_invalidate = [
            token
            for (token, token_user_id) in self.cache.items()
            if token_user_id == user_id
        ]
        for token in tokens_to_invalidate:
            self.cache.pop(token, None)
