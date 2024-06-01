from typing import List

from psycopg2._psycopg import Int

from core.domain.user.user_block_model import UserBlock


def get_blocked_user_ids(login_user_id: int) -> List[Int]:
    return [
        user_block.blocked_user
        for user_block in UserBlock.select().where(
            UserBlock.user == login_user_id, UserBlock.is_deleted == False
        )
    ]
