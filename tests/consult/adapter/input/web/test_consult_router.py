import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.consult.adapter.input.web.consult_router import consult_router
from app.user.domain.user import User
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from app.auth.domain.session import Session
from tests.user.fixtures.fake_user_repository import FakeUserRepository
from tests.auth.fixtures.fake_session_repository import FakeSessionRepository
from tests.consult.fixtures.fake_consult_repository import FakeConsultRepository


@pytest.fixture
def app():
    """FastAPI 앱"""
    app = FastAPI()
    app.include_router(consult_router, prefix="/consult")
    return app


@pytest.fixture
def user_repo():
    """테스트용 User 저장소"""
    return FakeUserRepository()


@pytest.fixture
def session_repo():
    """테스트용 Session 저장소"""
    return FakeSessionRepository()


@pytest.fixture
def consult_repo():
    """테스트용 Consult 저장소"""
    return FakeConsultRepository()


@pytest.fixture
def client(app, user_repo, session_repo, consult_repo):
    """테스트 클라이언트"""
    # 의존성 주입 (간단하게 global 변수 사용)
    from app.consult.adapter.input.web import consult_router as router_module
    from app.auth.adapter.input.web import auth_dependency

    router_module._user_repository = user_repo
    router_module._consult_repository = consult_repo
    auth_dependency._session_repository = session_repo

    return TestClient(app)


def test_start_consult_returns_session_id(client, user_repo, session_repo):
    """인증된 사용자가 상담을 시작하면 세션 ID를 반환한다"""
    # Given: 로그인한 사용자
    user = User(
        id="user-123",
        email="test@example.com",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE")
    )
    user_repo.save(user)

    # Given: 유효한 세션
    session = Session(session_id="valid-session-123", user_id="user-123")
    session_repo.save(session)

    # When: 상담 시작 API를 호출하면
    response = client.post(
        "/consult/start",
        headers={"Authorization": "Bearer valid-session-123"}
    )

    # Then: 200 OK와 세션 ID를 반환한다
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["session_id"] is not None


def test_start_consult_without_auth_returns_401(client):
    """인증 없이 상담을 시작하면 401을 반환한다"""
    # When: Authorization 헤더 없이 API를 호출하면
    response = client.post("/consult/start")

    # Then: 401 Unauthorized를 반환한다
    assert response.status_code == 401


def test_start_consult_with_invalid_session_returns_401(client):
    """잘못된 세션으로 상담을 시작하면 401을 반환한다"""
    # When: 잘못된 세션으로 API를 호출하면
    response = client.post(
        "/consult/start",
        headers={"Authorization": "Bearer invalid-session"}
    )

    # Then: 401 Unauthorized를 반환한다
    assert response.status_code == 401


def test_start_consult_without_user_profile_returns_400(client, user_repo, session_repo):
    """MBTI/Gender가 없는 사용자는 400을 반환한다"""
    # Given: MBTI/Gender가 없는 사용자
    user = User(id="user-123", email="test@example.com")
    user_repo.save(user)

    # Given: 유효한 세션
    session = Session(session_id="valid-session-123", user_id="user-123")
    session_repo.save(session)

    # When: 상담 시작 API를 호출하면
    response = client.post(
        "/consult/start",
        headers={"Authorization": "Bearer valid-session-123"}
    )

    # Then: 400 Bad Request를 반환한다
    assert response.status_code == 400
