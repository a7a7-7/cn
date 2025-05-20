import datetime
import os
from notion_client import Client

# 주간 일정 정의
weekly_schedule = {
    '월요일': {
        '오전': '백준 풀기',
        '점심': '알고리즘/하고싶은거 공부',
        '오후': '뉴로우',
        '저녁 과목': '수학, 알고리즘, 프로그래밍',
        '저녁 할거': '듀오링고, 영어 단어 / 발표 연습'
    },
    '화요일': {
        '오전': '백준 풀기',
        '점심': '알고리즘/하고싶은거 공부',
        '오후': '뉴로우',
        '저녁 과목': '영어, 컴구',
        '저녁 할거': '듀오링고, 영어 단어 / 발표 연습'
    },
    '수요일': {
        '오전': '백준 풀기',
        '점심': '알고리즘/하고싶은거 공부',
        '오후': '뉴로우',
        '저녁 과목': '수학, 알고리즘, 프로그래밍, 알고리즘',
        '저녁 할거': '듀오링고, 영어 단어 / 발표 연습'
    },
    '목요일': {
        '오전': '백준 풀기',
        '점심': '알고리즘/하고싶은거 공부',
        '오후': '뉴로우',
        '저녁 과목': '영어, 컴구',
        '저녁 할거': '듀오링고, 영어 단어 / 발표 연습'
    },
    '금요일': {
        '오전': '백준 풀기',
        '점심': '알고리즘/하고싶은거 공부',
        '오후': '뉴로우',
        '저녁 과목': '수학, 영어',
        '저녁 할거': '듀오링고, 영어 단어 / 발표 연습'
    }
}

# Notion API 연결
notion = Client(auth=os.environ["NOTION"])
database_id = os.environ["DB_ID"]

# 오늘 요일 확인
weekday_kor = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
today_kor = weekday_kor[datetime.datetime.utcnow().weekday()]  # GitHub은 UTC 기준

# 오늘 할 일 가져오기
tasks = weekly_schedule.get(today_kor, {})

# Notion에 추가
for time_slot, task in tasks.items():
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": f"[{time_slot}] {task}"
                        }
                    }
                ]
            },
            "상태": {
                "select": {
                    "name": "할 일"
                }
            }
        }
    )
