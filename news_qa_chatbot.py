import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from crawling import crawl_titles_presses_links, extract_news
import re

# .env 파일에서 API 키 불러오기
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)


# 이름 정리 함수
def trim_name(name):
    return re.sub(r'[^가-힣a-zA-Z0-9]+', '', name)


st.set_page_config(page_title="뉴스 요약 챗봇", page_icon="📰")
st.title("📰 금융 뉴스 요약 챗봇")

# 크롤링
titles, presses, links = crawl_titles_presses_links()

# 사이드바 기사 목록
with st.sidebar:
    st.header("🗞️ 오늘의 뉴스")
    selected = st.radio("기사를 선택하세요", options=titles[:10])

# 뉴스 선택 시 처리
# if selected:
#     idx = titles.index(selected)
#     title = titles[idx]
#     press = presses[idx]
#     link = links[idx]
#     news_text, date = extract_news(link)

#     st.subheader(f"📌 {title}")
#     st.markdown(f"🗓️ {date} | 🏷️ {press}")
#     with st.expander("📰 기사 전문 보기"):
#         st.write(news_text)

#     user_input = st.text_input("궁금한 점을 입력하세요 (예: 요약해줘)", key="question")

#     if user_input:
#         with st.spinner("🤖 GPT가 답변 중입니다..."):
#             try:
#                 completion = client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": "너는 사용자 질문에 간결하고 친절하게 요약/답변해주는 금융 뉴스 챗봇이야. 답변은 3문장 이내로 해줘."},
#                         {"role": "user", "content": f"다음 뉴스 내용을 참고해서 질문에 답해줘:\n\n{news_text}\n\n질문: {user_input}"}
#                     ]
#                 )
#                 response = completion.choices[0].message.content
#                 st.success("🧠 GPT의 답변")
#                 st.write(response)
#             except Exception as e:
#                 st.error(f"❌ 오류 발생: {str(e)}")
# 뉴스 선택 시 처리
if selected:
    idx = titles.index(selected)
    title = titles[idx]
    press = presses[idx]
    link = links[idx]
    news_text, date = extract_news(link)

    # 기사 선택 변경 시 입력 초기화
    if "last_selected" not in st.session_state or st.session_state.last_selected != selected:
        st.session_state.last_selected = selected
        st.session_state.question = ""
        st.session_state.response = ""

    st.subheader(f"📌 {title}")
    st.markdown(f"🗓️ {date} | 🏷️ {press}")
    with st.expander("📰 기사 전문 보기"):
        st.write(news_text)

    user_input = st.text_input("궁금한 점을 입력하세요 (예: 요약해줘)", key="question")

    if user_input and user_input != st.session_state.get("last_input", ""):
        st.session_state.last_input = user_input  # 이전 질문 저장
    # GPT 호출 로직 실행
    # if user_input and not st.session_state.get("response"):
        with st.spinner("🤖 GPT가 답변 중입니다..."):
            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "너는 사용자 질문에 간결하고 친절하게 요약/답변해주는 금융 뉴스 챗봇이야. 답변은 5문장 이내로 해줘."},
                         {"role": "user", "content": f"다음 뉴스 내용을 참고해서 질문에 답해줘:\n\n{news_text}\n\n질문: {user_input}"}
                    ]
                )
                st.session_state.response = completion.choices[0].message.content
            except Exception as e:
                st.session_state.response = f"❌ 오류 발생: {str(e)}"

    if st.session_state.get("response"):
        st.success("🧠 GPT의 답변")
        st.write(st.session_state.response)
