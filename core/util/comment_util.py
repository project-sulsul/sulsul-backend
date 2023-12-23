from typing import Optional, List

from fastapi import HTTPException
from starlette import status

from core.domain.comment_model import Comment
from core.dto.comment_dto import CommentResponse, CommentDto


class CommentValidator:
    @staticmethod
    def check_if_writeable(
        comment_id: int, comment: Optional[Comment], login_user_id: int
    ):
        if comment is None or comment.is_deleted is True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"comment(id:{comment_id}) is not found",
            )

        if comment.user_id != login_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"comment(id:{comment_id}) is not yours",
            )


class CommentBuilder:
    @staticmethod
    def layering(
        login_user_id: int, comments: List[CommentDto]
    ) -> List[CommentResponse]:
        parent_comments: List[CommentDto] = [
            comment for comment in comments if comment.parent_comment is None
        ]

        parent_to_children = CommentBuilder._parent_to_children_dict(
            comments, parent_comments
        )

        result = []

        for parent_comment in parent_comments:
            parent_id = parent_comment.id
            children = parent_to_children[parent_id]
            children_comments = CommentBuilder._build_children(children, login_user_id)
            is_writer = parent_comment.user == login_user_id

            parent_comment_response = CommentResponse.of_dict(
                comment=parent_comment,
                children_comments=children_comments,
                is_writer=is_writer,
            )

            result.append(parent_comment_response)

        return result

    @staticmethod
    def _parent_to_children_dict(
        comments: List[CommentDto], parent_comments: List[CommentDto]
    ) -> dict:
        parent_to_children = {comment.id: [] for comment in parent_comments}

        for comment in comments:
            if comment.parent_comment is not None:
                parent_to_children[comment.parent_comment].append(comment)

        return parent_to_children

    @staticmethod
    def _build_children(
        children: List[CommentDto], login_user_id: int
    ) -> List[CommentResponse]:
        children_comments = []

        for child in children:
            is_writer = child.user == login_user_id
            child_comment = CommentResponse.of_dict(comment=child, is_writer=is_writer)
            children_comments.append(child_comment)

        children_comments.sort(key=lambda comment: comment.created_at)

        return children_comments
