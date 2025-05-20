import os
import datetime
from notion_client import Client

notion = Client(auth=os.environ["NOTION"])
PAGE_ID = os.environ["DB_ID"]  # 표가 있는 일반 페이지의 ID

weekday_kor = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
today_kor = weekday_kor[datetime.datetime.utcnow().weekday()]
today_str = datetime.datetime.now().strftime("%Y-%m-%d (%a)")

# ✅ 표에서 오늘 열의 일정 추출
def extract_tasks_from_schedule(schedule_page_id, today):
    blocks = notion.blocks.children.list(block_id=schedule_page_id, page_size=100)
    table_block = next((b for b in blocks["results"] if b["type"] == "table"), None)
    if not table_block:
        return []
    rows = notion.blocks.children.list(block_id=table_block["id"])['results']
    header_cells = rows[0]["table_row"]["cells"]
    col_idx = next((i for i, cell in enumerate(header_cells) if cell and cell[0]['plain_text'] == today), None)
    if col_idx is None:
        return []

    results = []
    for row in rows[1:]:
        cells = row["table_row"]["cells"]
        if col_idx < len(cells) and cells[col_idx]:
            label = cells[0][0]['plain_text'] if cells[0] else "시간 미지정"
            task = cells[col_idx][0]['plain_text']
            results.append(f"[{label}] {task}")
    return results

# ✅ 기존 페이지 안에 블록 추가
def append_daily_todo_block(page_id, title, todo_list):
    blocks = []

    # 제목 블록
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": title}}]
        }
    })

    # To-do 블록들
    for task in todo_list:
        blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": task}}],
                "checked": False
            }
        })

    # 사용자 추가 안내 블록
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "📝 자유롭게 추가해 주세요!"}}]
        }
    })

    # 페이지에 블록 추가
    notion.blocks.children.append(block_id=page_id, children=blocks)


# ✅ 실행
tasks = extract_tasks_from_schedule(PAGE_ID, today_kor)
title = f"📋 {today_str} To-do 리스트"
append_daily_todo_block(PAGE_ID, title, tasks)
