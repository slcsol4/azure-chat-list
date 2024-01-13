# 以下を「app.py」に書き込み
import os
import streamlit as st
import openai

openai.api_type = "azure"
openai.api_base = "https://unoyuu-instance.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.environ.get('UNOYU_GPT4_API_KEY')

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
   st.session_state["messages"] = []

# チャットボットとやりとりする関数
def communicate():
    post_messages = [
        {"role": "system", "content": prompt}
    ]
    messages = st.session_state["messages"]
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)
    post_messages += messages
    response = openai.ChatCompletion.create(
               engine="unoyu-gpt-4",
               messages=post_messages,
  temperature=temperature,
  max_tokens=max_tokens,
  top_p=top_p,
  stop=None
              )
    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.set_page_config(
    layout="wide", 
    initial_sidebar_state="auto")

# メインエリア
st.title(" ソリューション本部 生成AI チャットボット")
# st.image("future.png")
# st.write("どんな食事を作りたいですか？")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
# サイドバー
st.sidebar.title("システム設定")
prompt = st.sidebar.text_area("プロンプト設定エリア", key="prompt")
max_tokens = st.sidebar.slider("最大応答トークン数", 1, 5000, 1000, 1)
st.sidebar.caption('モデル応答あたりのトークン数に制限を設定します。API は、プロンプト (システム メッセージ、例、メッセージ履歴、ユーザー クエリを含む) とモデルの応答の間で共有される最大の MaxTokensPlaceholderDoNotTranslate 個のトークンをサポートします。1 つのトークンは、一般的な英語テキストの約 4 文字です。')
temperature = st.sidebar.slider("温度", 0.0, 1.0, 0.0, 0.1)
st.sidebar.caption('ランダム性を制御します。温度を下げることは、モデルがより反復的および決定論的な応答を生成することを意味します。温度を上げると、予期しない応答や創造的な応答が増えます。温度または上位 P の両方ではなくどちらかを調整してみてください。')
top_p = st.sidebar.slider("上位P", 0.0, 1.0, 0.0, 0.1)
st.sidebar.caption('温度と同様に、これはランダム性を制御しますが、別の方法を使用します。上位 P を下げると、モデルのトークンの選択がより可能性が高いトークンに絞り込まれます。上位 P を上げると、確率が高いトークンと低いトークンの両方からモデルが選択できるようになります。温度または上位 P の両方ではなくどちらかを調整してみてください。')
