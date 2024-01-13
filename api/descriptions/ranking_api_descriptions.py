GET_COMBINATION_RANKING_DESC = """
조합 랭킹 조회 - 메인 화면의 좋아요 많은 조합 또는 색다른 조합  

- order_by_popular: bool (default: true) - 해당 쿼리 파라미터가 없으면 좋아요 많은 순으로 조회합니다. false 시 색다른 조합 순으로 조회합니다
- 개수는 3개까지 조회됩니다.
- 임시로 전체 기간 동안의 피드로 랭킹을 집계합니다
"""

GET_ALCOHOL_RANKING_DESC = """
술 랭킹 조회 - 랭킹 화면의 술 랭킹  

- 술 랭킹(전체)을 조회합니다
- 임시로 전체 기간 동안의 피드로 랭킹을 집계합니다
"""

GET_TAGS_RELATED_FEEDS_DESC = """
랭킹 아이템 상세 조회 - 태그 관련 피드 조회 (화면상 포함피드)

- 로그인 정보가 존재하면 is_liked 정보가 로그인 유저 기준으로 반영됩니다.
- tags를 여러개 넘기고 싶으면 콤마로 분리해주세요 (ex. 삼겹살,소주)
- tags는 classify_tags를 의미합니다.
- tags는 한글로 입력해주세요
"""
