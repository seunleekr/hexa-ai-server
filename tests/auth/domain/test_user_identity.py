import pytest
from app.auth.domain.user_identity import UserIdentity


def test_create_user_identity_with_valid_values():
    """유효한 user_id, provider, provider_user_id로 UserIdentity 객체를 생성할 수 있다"""
    # Given: 유효한 값들
    user_id = "user-123"
    provider = "google"
    provider_user_id = "google-abc-xyz"

    # When: UserIdentity 객체를 생성하면
    identity = UserIdentity(
        user_id=user_id,
        provider=provider,
        provider_user_id=provider_user_id
    )

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert identity.user_id == "user-123"
    assert identity.provider == "google"
    assert identity.provider_user_id == "google-abc-xyz"


def test_reject_empty_user_id():
    """빈 user_id를 거부한다"""
    # Given: 빈 user_id
    user_id = ""
    provider = "google"
    provider_user_id = "google-abc-xyz"

    # When & Then: UserIdentity 객체 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        UserIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id)


def test_reject_empty_provider():
    """빈 provider를 거부한다"""
    # Given: 빈 provider
    user_id = "user-123"
    provider = ""
    provider_user_id = "google-abc-xyz"

    # When & Then: UserIdentity 객체 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        UserIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id)


def test_reject_empty_provider_user_id():
    """빈 provider_user_id를 거부한다"""
    # Given: 빈 provider_user_id
    user_id = "user-123"
    provider = "google"
    provider_user_id = ""

    # When & Then: UserIdentity 객체 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        UserIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id)


def test_accept_google_provider():
    """유효한 provider 'google'을 허용한다"""
    # Given: google provider
    user_id = "user-123"
    provider = "google"
    provider_user_id = "google-abc-xyz"

    # When: UserIdentity 객체를 생성하면
    identity = UserIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id)

    # Then: 정상적으로 생성된다
    assert identity.provider == "google"


def test_accept_kakao_provider():
    """유효한 provider 'kakao'를 허용한다"""
    # Given: kakao provider
    user_id = "user-123"
    provider = "kakao"
    provider_user_id = "kakao-def-uvw"

    # When: UserIdentity 객체를 생성하면
    identity = UserIdentity(user_id=user_id, provider=provider, provider_user_id=provider_user_id)

    # Then: 정상적으로 생성된다
    assert identity.provider == "kakao"


def test_reject_invalid_provider():
    """유효하지 않은 provider를 거부한다"""
    # Given: 유효하지 않은 provider들
    user_id = "user-123"
    provider_user_id = "some-user-id"
    invalid_providers = ["facebook", "twitter", "naver", "GOOGLE", "KAKAO"]

    # When & Then: UserIdentity 객체 생성 시 ValueError가 발생한다
    for invalid_provider in invalid_providers:
        with pytest.raises(ValueError):
            UserIdentity(user_id=user_id, provider=invalid_provider, provider_user_id=provider_user_id)
