import streamlit as st
from openai import OpenAI

# 🔒 비밀번호 설정
PASSWORD = "qwerty"

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ✅ 로그인 상태가 아니면 로그인 페이지만 보여줌
if not st.session_state["authenticated"]:
    st.title("🔐 비밀번호가 필요합니다")
    password = st.text_input("비밀번호를 입력하세요:", type="password")
    
    if password == PASSWORD:
        st.session_state["authenticated"] = True  # 다음 렌더링부터 챗봇 화면으로 전환됨
        st.success("비밀번호가 맞습니다! 아래 버튼을 눌러주세요.")
        st.button("👉 계속하기")  # 다음 렌더링 유도용 버튼
    elif password:
        st.error("비밀번호가 틀렸어요. 다시 시도해보세요.")
# 로딩 화면
elif not st.session_state["loading_done"]:
    st.title("🔄 로딩 중입니다...")
    progress = st.progress(0, text="잠시만 기다려 주세요...")

    # 파란 막대 애니메이션
    for percent in range(101):
        time.sleep(0.01)  # 속도 조절
        progress.progress(percent, text=f"불러오는 중... {percent}%")

    st.session_state["loading_done"] = True
    st.rerun()
# ✅ 로그인 성공하면 챗봇 페이지
if st.session_state["authenticated"]:
    st.title("Yoon Teacher's chatbot")

    client = OpenAI()

    tone = st.radio("대화방식 선택:", ("높임말", "반말"), horizontal=True)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4.1"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("지금 기분은 어때?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if tone == "높임말":
            system_prompt = {
                "role": "system",
                "content": "당신은 초등학교 선생님입니다. 공손하고 따뜻한 높임말로 대답해주세요."
            }
        else:
            system_prompt = {
                "role": "system",
                "content": "너는 초등학생 친구처럼 반말로 편하게 대답해."
            }

        with st.chat_message("assistant"):
            full_response = ""
            placeholder = st.empty()

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[system_prompt] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
