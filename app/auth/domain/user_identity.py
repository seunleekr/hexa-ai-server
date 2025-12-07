class UserIdentity:
    """OAuth provider와 user를 연결하는 도메인 객체"""

    _VALID_PROVIDERS = ["google", "kakao"]

    def __init__(self, user_id: str, provider: str, provider_user_id: str):
        self._validate(user_id, provider, provider_user_id)
        self.user_id = user_id
        self.provider = provider
        self.provider_user_id = provider_user_id

    def _validate(self, user_id: str, provider: str, provider_user_id: str) -> None:
        """UserIdentity 값의 유효성을 검증한다"""
        if not user_id:
            raise ValueError("user_id는 비어있을 수 없습니다")
        if not provider:
            raise ValueError("provider는 비어있을 수 없습니다")
        if provider not in self._VALID_PROVIDERS:
            valid_providers = "/".join(self._VALID_PROVIDERS)
            raise ValueError(f"provider는 {valid_providers} 중 하나여야 합니다: {provider}")
        if not provider_user_id:
            raise ValueError("provider_user_id는 비어있을 수 없습니다")
