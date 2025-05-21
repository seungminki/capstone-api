from openai import OpenAI
import re
from settings import OPENAI_TOKEN

client = OpenAI(
    api_key=OPENAI_TOKEN,
    # increase default timeout to 15 minutes (from 10 minutes)
    timeout=900.0,
)


def openai_api(text: str):
    post_text = preprocess(text)
    prompt_template = create_prompt(post_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 텍스트를 주제별로 정확히 분류하는 도우미입니다.",
            },
            {"role": "user", "content": prompt_template},
        ],
        temperature=0.1,
    )
    content = response.choices[0].message.content

    return postprocess(content)


def preprocess(text: str):
    pattern = re.compile(r"[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z\s]")  # 한글, 영어
    post_text = pattern.sub("", text).strip()

    return post_text


def postprocess(text: str):
    pattern = r'카테고리:\s*"?(.+?)"?$'

    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return "None"


def create_prompt(post_text: str):
    # gpt_tagging_list_v1
    # 주제 목록 이후 리스트에 따라 결과물이 달라질 수 있음
    # TODO: db에 prompt version 함께 입력
    prompt_template = f"""
    다음은 대학 커뮤니티 게시판에 올라온 게시글입니다.

    ---

    게시글 내용:  
    "{post_text}"

    ---

    다음 주제 중 하나로 이 게시글을 분류하세요.  
    해당되는 주제가 없으면 **"해당 없음"** 이라고 답하세요.  
    복수 선택은 하지 말고 가장 적합한 하나의 주제만 선택하세요.

    주제 목록:
    1. 생활 정보 (기숙사, 자취, 요리, 식사, 디지털, 카페 등)
    2. 커뮤니티 소통 (연애, 고민, 질문, 조언, 소통, 모임 등)
    3. 중고/거래/나눔 (판매, 중고거래, 나눔, 구함 등)
    4. 건강/운동 (다이어트, 운동, 체중 감량, 헬스 등)
    5. 안전/유실물 (분실물, 도난, 안전, 문의 등)
    6. 캠퍼스 주변 정보 (통학, 교통, 지역 정보 등)
    7. 추천/후기 (맛집 추천, 기기 후기, 장소 평가 등)

    ---

    출력 형식 (그대로 따라하세요):  
    카테고리: {{여기에 주제를 써주세요, 예: "생활 정보" 또는 "해당 없음"}}
    """
    return prompt_template
