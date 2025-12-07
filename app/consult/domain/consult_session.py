from datetime import datetime
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender


class ConsultSession:
    """상담 세션 도메인 엔티티"""

    def __init__(
        self,
        id: str,
        user_id: str,
        mbti: MBTI,
        gender: Gender,
        created_at: datetime | None = None,
    ):
        self._validate(id, user_id, mbti, gender)
        self.id = id
        self.user_id = user_id
        self.mbti = mbti
        self.gender = gender
        self.created_at = created_at or datetime.now()

    def _validate(self, id: str, user_id: str, mbti: MBTI | None, gender: Gender | None) -> None:
        """ConsultSession 값의 유효성을 검증한다"""
        if not id:
            raise ValueError("ConsultSession id는 비어있을 수 없습니다")
        if not user_id:
            raise ValueError("ConsultSession user_id는 비어있을 수 없습니다")
        if mbti is None:
            raise ValueError("ConsultSession mbti는 None일 수 없습니다")
        if gender is None:
            raise ValueError("ConsultSession gender는 None일 수 없습니다")
