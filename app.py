import urllib.request
import json
import os
import ssl
import streamlit as st

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
url = 'https://unoyu-chat-list.japaneast.inference.ml.azure.com/score'
api_key = os.environ.get('CHAT_LIST_API_KEY')

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
   st.session_state["messages"] = []
#
def clearChat():
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    question = st.session_state["user_input"]

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'unoyu-chat-list-2' }
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = {
          'chat_history': messages,
          'question': question
    }

    body = str.encode(json.dumps(data))
    req = urllib.request.Request(url, body, headers)

    response = urllib.request.urlopen(req)
    read_response = response.read()
    output_message = json.loads(read_response)["output"]
    result = {
      'inputs':{'question': question},
      'outputs':{
        'line_number': len(messages) + 1,
        'output': output_message
      }
    }
    messages.append(result)
    st.session_state["user_input"] = ""  # 入力欄を消去



# ユーザーインターフェイスの構築
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto")

# メインエリア
st.title(" ソリューション本部 生成AI チャットボット")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
st.button('Clear All Chat', on_click=clearChat)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        # 回答内容を記載
        st.write("🤖" + ": " + message["outputs"]["output"])
        # 質問内容を記載
        st.write("🙂" + ": " + message["inputs"]["question"])

