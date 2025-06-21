import streamlit as st
from openai import OpenAI

# 🔒 비밀번호 설정
PASSWORD = "teacher123"

# 초기 세션 상태
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 🔐 로그인 페이지
if not st.session_state["authenticated"]:
    st.title("🔐 비밀번호가 필요합니다")
    password = st.text_input("비밀번호를 입력하세요:", type="password")
    if password == PASSWORD:
        st.success("비밀번호가 맞습니다! 🤗")
        st.session_state["authenticated"] = True
        st.experimental_rerun()
    elif password:
        st.error("비밀번호가 틀렸어요. 다시 시도해보세요.")

# ✅ 로그인 성공 시 챗봇 페이지로 "전환"
else:
    st.title("Yoon Teacher's chatbot")

    # 👇 여기에 챗봇 코드 시작
    client = OpenAI()

    tone = st.radio("말투 선택:", ("높임말", "반말"), horizontal=True)

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
