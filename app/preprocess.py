from soynlp.normalizer import repeat_normalize, emoticon_normalize

import re

pattern = re.compile(r"[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z\s]")  # 한글, 영어

letter_ko_pattern = re.compile(r"[^가-힣\s]")  # 한글 초성 제거

url_pattern = re.compile(r"https?://\S+")
dial_pattern = re.compile(r"010-\d{4}-\d{4}|041-\d{3}-\d{4}|02-\d{3}-\d{4}")
email_pattern = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
space_pattern = re.compile(r"\s+")


def preprocess(x):
    x = url_pattern.sub("", x)
    x = dial_pattern.sub("", x)
    x = email_pattern.sub("", x)

    x = pattern.sub("", x)
    x = letter_ko_pattern.sub("", x)

    x = space_pattern.sub(" ", x)
    x = x.strip()

    x = emoticon_normalize(x, num_repeats=2)
    x = repeat_normalize(x, num_repeats=1)

    return x
