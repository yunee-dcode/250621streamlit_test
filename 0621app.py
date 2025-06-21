from openai import OpenAI
import streamlit as st

st.title("👩‍🏫Yoonie Teacher's chatbot")

client = OpenAI()

# 말투 선택
tone = st.radio("원하는 말투를 선택하세요 👇", ("높임말", "반말"), horizontal=True)

# 모델 설정
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1"

# 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("지금 기분은 어때?"):

    # 입력 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # 말투에 따라 system prompt 설정
    if tone == "높임말":
        system_prompt = {
            "role": "system",
            "content": "당신은 초등학교 선생님입니다. 사용자의 질문에 공손하고 예의 바르게, 높임말로 답변해주세요."
        }
    else:  # 반말
        system_prompt = {
            "role": "system",
            "content": "너는 초등학생 친구랑 이야기하듯 친근하게 반말로 대답해. 너무 딱딱하지 않게, 재미있고 편하게 말해줘."
        }

    with st.chat_message("assistant"):
        full_response = ""

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
                st.write(content, end="")

        st.session_state.messages.append({"role": "assistant", "content": full_response})
