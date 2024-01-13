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

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'unoyu-chat-list-2' }
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data = {
          'chat_history': [
          {
            'inputs':{'question': 'スクラムマスターとプロダクトオーナーの意見が食い違った場合の対処方法は？'},
            'outputs':{'line_number': 0,
              'output':'スクラムガイドには、スクラムマスターとプロダクトオーナーの意見が食い違った場合の具体的な対処方法については明記されていません。しかし、スクラムマスターとプロダクトオーナーはそれぞれ異なる役割を持っています。プロダクトオーナーはプロダクトの価値を最大化することとプロダクトバックログ管理に責任を持ちます。一方、スクラムマスターはスクラムの理論とプラクティスを全員に理解してもらえるよう支援し、スクラムチームの有効性に責任を持ちます。したがって、意見が食い違った場合でも、それぞれの役割と責任を理解し尊重することが重要です。また、スクラムマスターはプロダクトオーナーを支援する役割も持っているため、対話や協議を通じて解決策を見つけることが求められます(Source: 2020-Scrum-Guide-Japanese.pdf).'
            }
           },
           {
            'inputs':{'question': 'スプリントの中でプロダクトオーナーが果たす役割と、スクラムマスターが果たす役割は？'},
            'outputs':{'line_number': 1,
              'output':'プロダクトオーナーは、スクラムチームから生み出されるプロダクトの価値を最大化することの結果に責任を持ちます。具体的には、プロダクトゴールを策定し明示的に伝え、プロダクトバックログアイテムを作成し明確に伝え、プロダクトバックログアイテムを並び替え、プロダクトバックログに透明性があり見える化され理解されるようにするなどの責任を持ちます。また、プロダクトオーナーは1人の人間であり、委員会ではないとされています(Source: 2020-Scrum-Guide-Japanese.pdf).\n\n一方、スクラムマスターは、スクラムガイドで定義されたスクラムを確実させることの結果に責任を持ちます。スクラムマスターは、スクラムチームと組織において、スクラムの理論とプラクティスを全員に理解してもらえるよう支援することで、その責任を果たします。また、スクラムマスターは、スクラムチームの有効性に責任を持ち、スクラムチームがスクラムフレームワーク内でプラクティスを改善できるようにすることで、その責任を果たします(Source: 2020-Scrum-Guide-Japanese.pdf).'
            }
           },
           {
            'inputs':{'question': '１スプリント期間内の役割について聞いています。'},
            'outputs':{'line_number': 2,
              'output':'スプリント期間中、プロダクトオーナーはプロダクトバックログアイテムの優先順位を設定し、スクラムチームと共にスプリントゴールを定義します。また、スプリントプランニングに参加し、スクラムチームに最も重要なプロダクトバックログアイテムとそれらとプロダクトゴールとの関連性について説明します。さらに、スプリントレビューではスプリントの成果を検査し、今後の適応を決定します(Source: 2020-Scrum-Guide-Japanese.pdf).\n\nスクラムマスターは、スプリント期間中にスクラムのプラクティスとルールが遵守されることを確認します。また、スクラムチームがポジティブで生産的であり、タイムボックスの制限が守られるようにする役割を果たします。さらに、スクラムマスターはスプリントレトロスペクティブを通じて、スクラムチームがスプリント中に何がうまくいったか、どのような問題が発生したか、そしてそれらの問題がどのように解決されたか（または解決されなかったか）について話し合う場を提供します(Source: 2020-Scrum-Guide-Japanese.pdf).'
            }
           },
           {
            'inputs':{'question': 'スプリント間をつなぐ工夫は？'},
            'outputs':{'line_number': 3,
              'output':'スクラムガイドには、スプリント間をつなぐ具体的な工夫については明記されていません。しかし、スクラムでは各スプリントが前のスプリントの直後に始まるとされています。これは、スプリント間にギャップを作らず、連続的な開発フローを維持することを意味します。また、各スプリントの終わりにはスプリントレビューとスプリントレトロスペクティブが行われ、これらは次のスプリントの計画に役立つ洞察を提供します。スプリントレビューでは、スプリントの成果が検査され、今後の適応が決定されます。スプリントレトロスペクティブでは、スクラムチームがスプリント中に何がうまくいったか、どのような問題が発生したか、そしてそれらの問題がどのように解決されたか（または解決されなかったか）について話し合います。これらの活動は、次のスプリントへの改善点を明らかにし、スプリント間の連続性を保つのに役立ちます(Source: 2020-Scrum-Guide-Japanese.pdf).'
            }
           }
        ],
        'question': st.session_state["user_input"]
    }

    body = str.encode(json.dumps(data))
    req = urllib.request.Request(url, body, headers)

    response = urllib.request.urlopen(req)
    bot_message = response.read()
    
    messages.append(bot_message)
    print(messages)
    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.set_page_config(
    layout="wide", 
    initial_sidebar_state="auto")

# メインエリア
st.title(" ソリューション本部 生成AI チャットボット")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
