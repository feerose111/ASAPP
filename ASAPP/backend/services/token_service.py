from typing import Set

class TokenService:
    """Simple in-memory token blacklist service"""

    _blacklist: Set[str] = set()

    @classmethod
    async def blacklist_token(cls, token: str) -> None:
        """Add token to blacklist"""
        cls._blacklist.add(token)

    @classmethod
    async def is_token_blacklisted(cls, token: str) -> bool:
        """Check if token is blacklisted"""
        return token in cls._blacklist

    @classmethod
    def clear_blacklist(cls) -> None:
        """Clear all blacklisted tokens (for testing)"""
        cls._blacklist.clear()

# Create instance
token_service = TokenService()