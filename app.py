import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import qrcode
import io
import json
from datetime import datetime, timedelta
import base64
from streamlit_option_menu import option_menu

# ページ設定
st.set_page_config(
    page_title="イベントポータル",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS - ナイトモード
st.markdown("""
<style>
    /* 全体のダークテーマ */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* サイドバーのダークテーマ */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* メインヘッダー */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* セッションカード */
    .session-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border-left: 4px solid #667eea;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
        transition: all 0.3s ease;
    }
    
    .session-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* 登壇者カード */
    .speaker-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
        transition: all 0.3s ease;
    }
    
    .speaker-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* FAQアイテム */
    .faq-item {
        background: linear-gradient(145deg, #1a1a1a, #2a2a2a);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 4px solid #28a745;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
    }
    
    /* チャットメッセージ */
    .chat-message {
        background: linear-gradient(145deg, #1e3a8a, #1e40af);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
    }
    
    /* メトリクスカード */
    .metric-card {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8, #6a4190);
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* セレクトボックスのスタイル */
    .stSelectbox > div > div {
        background-color: #2a2a2a;
        color: #fafafa;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* テキスト入力のスタイル */
    .stTextInput > div > div > input {
        background-color: #2a2a2a;
        color: #fafafa;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* テキストエリアのスタイル */
    .stTextArea > div > div > textarea {
        background-color: #2a2a2a;
        color: #fafafa;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* スライダーのスタイル */
    .stSlider > div > div > div > div {
        background-color: #2a2a2a;
    }
    
    /* リンクのスタイル */
    a {
        color: #667eea;
        text-decoration: none;
    }
    
    a:hover {
        color: #5a6fd8;
        text-decoration: underline;
    }
    
    /* 情報ボックスのスタイル */
    .stAlert {
        background: linear-gradient(145deg, #1e3a8a, #1e40af);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
    }
    
    /* 成功メッセージのスタイル */
    .stSuccess {
        background: linear-gradient(145deg, #065f46, #047857);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #fafafa;
    }
    
    /* エクスパンダーのスタイル */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        color: #fafafa;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* タブのスタイル */
    .stTabs > div > div > div > div {
        background-color: #2a2a2a;
        color: #fafafa;
    }
    
    /* プロットの背景 */
    .js-plotly-plot {
        background-color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'notes' not in st.session_state:
    st.session_state.notes = {}
if 'contacts' not in st.session_state:
    st.session_state.contacts = []

# サンプルデータ
def load_sample_data():
    # イベント概要
    event_info = {
        "name": "ノンプログラマーズ・テックキャンプ2025",
        "date": "2025年9月6日（土）",
        "time": "13:00 - 18:00",
        "venue": "サイボウズ",
        "address": "中央区日本橋２丁目７−１ 東京日本橋タワ ２７階",
        "organizer": "ノンプロ研",
        "description": "ノンプログラマーズ・テックキャンプ2025 ～AIやAppSheet、Excel活用術も学べる！業務改善・DXの祭典～"
    }
    
    # タイムテーブル
    timetable = [
        {"time": "12:00-12:45", "title": "開場・受付", "speaker": "-", "room": "ロビー"},
        {"time": "13:00-13:05", "title": "オープニング", "speaker": "田中太郎", "room": "メインホール"},
        {"time": "13:05-13:30", "title": "基調講演：", "speaker": "タカハシノリアキ", "room": "メインホール"},
        {"time": "11:15-12:15", "title": "セッションA：", "speaker": "鈴木一郎", "room": "会議室A"},
        {"time": "11:15-12:15", "title": "セッションB：", "speaker": "高橋美咲", "room": "会議室B"},
        {"time": "12:15-13:30", "title": "ランチブレイク", "speaker": "-", "room": "レストラン"},
        {"time": "13:30-14:30", "title": "パネルディスカッション", "speaker": "パネリスト", "room": "メインホール"},
        {"time": "14:45-15:45", "title": "ワークショップ", "speaker": "山田次郎", "room": "ワークショップ室"},
        {"time": "16:00-17:00", "title": "ネットワーキング", "speaker": "-", "room": "ロビー"},
        {"time": "17:00-18:00", "title": "クロージング", "speaker": "田中太郎", "room": "メインホール"}
    ]
    
    # 登壇者情報
    speakers = [
        {
            "name": "田中太郎",
            "title": "CEO",
            "company": "Tech Corp",
            "bio": "20年以上のIT業界経験を持つエキスパート",
            "sessions": ["オープニング", "クロージング"],
            "twitter": "@tanaka_taro",
            "linkedin": "linkedin.com/in/tanaka-taro"
        },
        {
            "name": "佐藤花子",
            "title": "CTO",
            "company": "AI Solutions",
            "bio": "AI・機械学習の専門家",
            "sessions": ["基調講演：AIの未来"],
            "twitter": "@sato_hanako",
            "linkedin": "linkedin.com/in/sato-hanako"
        },
        {
            "name": "鈴木一郎",
            "title": "エンジニア",
            "company": "Cloud Tech",
            "bio": "クラウドインフラのエキスパート",
            "sessions": ["セッションA：クラウド技術"],
            "twitter": "@suzuki_ichiro",
            "linkedin": "linkedin.com/in/suzuki-ichiro"
        },
        {
            "name": "高橋美咲",
            "title": "リサーチャー",
            "company": "Blockchain Lab",
            "bio": "ブロックチェーン技術の研究者",
            "sessions": ["セッションB：ブロックチェーン"],
            "twitter": "@takahashi_misaki",
            "linkedin": "linkedin.com/in/takahashi-misaki"
        }
    ]
    
    # FAQ
    faq = [
        {"question": "参加費はいくらですか？", "answer": "一般参加：5,000円、学生：2,000円"},
        {"question": "事前登録は必要ですか？", "answer": "はい、事前登録をお願いします。"},
        {"question": "Wi-Fiは利用できますか？", "answer": "はい、会場内で無料Wi-Fiをご利用いただけます。"},
        {"question": "資料は後日ダウンロードできますか？", "answer": "はい、イベント後1週間以内にダウンロード可能です。"}
    ]
    
    return event_info, timetable, speakers, faq

# データ読み込み
event_info, timetable, speakers, faq = load_sample_data()

# サイドバーメニュー
with st.sidebar:
    st.title("🎪 イベントポータル")
    
    selected = option_menu(
        "メニュー",
        ["🏠 ホーム", "📅 タイムテーブル", "👥 登壇者", "🗺️ 会場マップ", "❓ FAQ", 
         "📁 資料ダウンロード", "📝 アンケート", "💬 チャット", "📇 名刺交換", "📝 メモ"],
        icons=['house', 'calendar', 'people', 'map', 'question-circle', 
               'folder', 'clipboard', 'chat', 'card-text', 'pencil'],
        menu_icon="cast",
        default_index=0,
    )

# ホームページ
if selected == "🏠 ホーム":
    st.markdown('<div class="main-header"><h1>ノンプログラマーズ・テックキャンプ2025</h1><p>～AIやAppSheet、Excel活用術も学べる！業務改善・DXの祭典～</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 イベント概要")
        st.write(f"**日時:** {event_info['date']} {event_info['time']}")
        st.write(f"**会場:** {event_info['venue']}")
        st.write(f"**住所:** {event_info['address']}")
        st.write(f"**主催:** {event_info['organizer']}")
        st.write(f"**概要:** {event_info['description']}")
        
        st.subheader("🚀 今日のハイライト")
        highlights = [
            "基調講演：AIの未来",
            "パネルディスカッション",
            "ワークショップ",
            "ネットワーキング"
        ]
        for highlight in highlights:
            st.write(f"• {highlight}")
    
    with col2:
        st.subheader("📊 イベント統計")
        stats_data = {
            "参加者数": 150,
            "登壇者数": 4,
            "セッション数": 8,
            "会場数": 3
        }
        
        for stat, value in stats_data.items():
            col_a, col_b = st.columns([2, 1])
            col_a.markdown(f'<div class="metric-card"><strong>{stat}</strong></div>', unsafe_allow_html=True)
            col_b.metric("", value)
        
        st.subheader("⏰ 次のセッション")
        current_time = datetime.now()
        next_session = None
        for session in timetable:
            if session["time"].split("-")[0] > current_time.strftime("%H:%M"):
                next_session = session
                break
        
        if next_session:
            st.info(f"**{next_session['time']}** - {next_session['title']}")

# タイムテーブルページ
elif selected == "📅 タイムテーブル":
    st.title("📅 タイムテーブル")
    
    # フィルター
    col1, col2 = st.columns(2)
    with col1:
        room_filter = st.selectbox("会場で絞り込み", ["すべて", "メインホール", "会議室A", "会議室B", "ワークショップ室", "ロビー", "レストラン"])
    with col2:
        time_filter = st.selectbox("時間帯で絞り込み", ["すべて", "午前", "午後"])
    
    # タイムテーブル表示
    filtered_timetable = timetable
    if room_filter != "すべて":
        filtered_timetable = [s for s in filtered_timetable if s["room"] == room_filter]
    
    if time_filter == "午前":
        filtered_timetable = [s for s in filtered_timetable if s["time"].split("-")[0] < "12:00"]
    elif time_filter == "午後":
        filtered_timetable = [s for s in filtered_timetable if s["time"].split("-")[0] >= "12:00"]
    
    for session in filtered_timetable:
        with st.container():
            st.markdown(f"""
            <div class="session-card">
                <h4>{session['time']} - {session['title']}</h4>
                <p><strong>登壇者:</strong> {session['speaker']}</p>
                <p><strong>会場:</strong> {session['room']}</p>
            </div>
            """, unsafe_allow_html=True)

# 登壇者ページ
elif selected == "👥 登壇者":
    st.title("👥 登壇者一覧")
    
    # 検索機能
    search = st.text_input("登壇者を検索", placeholder="名前、会社名、セッション名で検索")
    
    # 登壇者カード表示
    cols = st.columns(2)
    for i, speaker in enumerate(speakers):
        if search.lower() in speaker['name'].lower() or search.lower() in speaker['company'].lower() or any(search.lower() in session.lower() for session in speaker['sessions']):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="speaker-card">
                    <h4>{speaker['name']}</h4>
                    <p><strong>{speaker['title']}</strong> at {speaker['company']}</p>
                    <p>{speaker['bio']}</p>
                    <p><strong>登壇セッション:</strong></p>
                    <ul>
                        {''.join([f'<li>{session}</li>' for session in speaker['sessions']])}
                    </ul>
                    <p>🐦 <a href="https://twitter.com/{speaker['twitter'].replace('@', '')}" target="_blank">{speaker['twitter']}</a></p>
                    <p>💼 <a href="https://{speaker['linkedin']}" target="_blank">LinkedIn</a></p>
                </div>
                """, unsafe_allow_html=True)

# 会場マップページ
elif selected == "🗺️ 会場マップ":
    st.title("🗺️ 会場マップ・アクセス情報")
    
    tab1, tab2, tab3 = st.tabs(["🏢 フロアマップ", "🚇 アクセス", "🏪 近隣施設"])
    
    with tab1:
        st.subheader("フロアマップ")
        
        # 簡易的なフロアマップ（実際のアプリでは画像を使用）
        floor_map_data = {
            "メインホール": {"x": 50, "y": 30, "capacity": 200},
            "会議室A": {"x": 20, "y": 60, "capacity": 50},
            "会議室B": {"x": 80, "y": 60, "capacity": 50},
            "ワークショップ室": {"x": 50, "y": 80, "capacity": 30},
            "ロビー": {"x": 50, "y": 10, "capacity": 100},
            "レストラン": {"x": 20, "y": 10, "capacity": 80}
        }
        
        # Plotlyでフロアマップを作成
        fig = go.Figure()
        
        for room, info in floor_map_data.items():
            fig.add_trace(go.Scatter(
                x=[info["x"]],
                y=[info["y"]],
                mode='markers+text',
                marker=dict(size=20, color='lightblue'),
                text=room,
                textposition="middle center",
                name=room,
                hovertemplate=f"<b>{room}</b><br>収容人数: {info['capacity']}人<extra></extra>"
            ))
        
        fig.update_layout(
            title="フロアマップ",
            xaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
            yaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fafafa')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("アクセス情報")
        st.write("**会場:** 東京国際フォーラム")
        st.write("**住所:** 東京都千代田区丸の内3-5-1")
        st.write("**最寄り駅:**")
        st.write("• JR有楽町駅（徒歩5分）")
        st.write("• 東京メトロ有楽町線有楽町駅（徒歩5分）")
        st.write("• 東京メトロ日比谷線日比谷駅（徒歩7分）")
        
        # 地図の埋め込み（実際のアプリではGoogle Maps APIを使用）
        st.map(pd.DataFrame({
            'lat': [35.6748],
            'lon': [139.7648]
        }), use_container_width=True)
    
    with tab3:
        st.subheader("近隣施設")
        facilities = [
            {"name": "コンビニ", "distance": "徒歩3分", "description": "セブンイレブン"},
            {"name": "カフェ", "distance": "徒歩5分", "description": "スターバックス"},
            {"name": "レストラン", "distance": "徒歩7分", "description": "和食レストラン"},
            {"name": "ATM", "distance": "徒歩2分", "description": "三菱UFJ銀行"}
        ]
        
        for facility in facilities:
            st.write(f"**{facility['name']}** ({facility['distance']}) - {facility['description']}")

# FAQページ
elif selected == "❓ FAQ":
    st.title("❓ よくある質問（FAQ）")
    
    # 検索機能
    faq_search = st.text_input("質問を検索", placeholder="キーワードを入力")
    
    for item in faq:
        if faq_search.lower() in item['question'].lower() or faq_search.lower() in item['answer'].lower():
            with st.expander(item['question']):
                st.write(item['answer'])

# 資料ダウンロードページ
elif selected == "📁 資料ダウンロード":
    st.title("📁 資料ダウンロード")
    
    # サンプル資料データ
    documents = [
        {"name": "基調講演資料.pdf", "session": "基調講演：AIの未来", "speaker": "佐藤花子", "size": "2.5MB", "downloads": 45},
        {"name": "クラウド技術セッション資料.pdf", "session": "セッションA：クラウド技術", "speaker": "鈴木一郎", "size": "1.8MB", "downloads": 32},
        {"name": "ブロックチェーン技術資料.pdf", "session": "セッションB：ブロックチェーン", "speaker": "高橋美咲", "size": "3.2MB", "downloads": 28},
        {"name": "ワークショップ資料.zip", "session": "ワークショップ", "speaker": "山田次郎", "size": "15.6MB", "downloads": 67}
    ]
    
    # フィルター
    col1, col2 = st.columns(2)
    with col1:
        session_filter = st.selectbox("セッションで絞り込み", ["すべて"] + list(set([doc["session"] for doc in documents])))
    with col2:
        speaker_filter = st.selectbox("登壇者で絞り込み", ["すべて"] + list(set([doc["speaker"] for doc in documents])))
    
    # 資料一覧表示
    filtered_docs = documents
    if session_filter != "すべて":
        filtered_docs = [doc for doc in filtered_docs if doc["session"] == session_filter]
    if speaker_filter != "すべて":
        filtered_docs = [doc for doc in filtered_docs if doc["speaker"] == speaker_filter]
    
    for doc in filtered_docs:
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        col1.write(f"**{doc['name']}**")
        col2.write(doc['session'])
        col3.write(doc['size'])
        col4.write(f"📥 {doc['downloads']}")
        
        if st.button(f"ダウンロード", key=doc['name']):
            st.success("ダウンロードを開始しました！")

# アンケートページ
elif selected == "📝 アンケート":
    st.title("📝 アンケート")
    
    tab1, tab2 = st.tabs(["イベント全体", "セッション別"])
    
    with tab1:
        st.subheader("イベント全体の満足度調査")
        
        overall_satisfaction = st.slider("全体の満足度", 1, 5, 3)
        st.write(f"選択された値: {overall_satisfaction}")
        
        content_quality = st.selectbox("コンテンツの質", ["非常に良い", "良い", "普通", "悪い", "非常に悪い"])
        venue_satisfaction = st.selectbox("会場の満足度", ["非常に良い", "良い", "普通", "悪い", "非常に悪い"])
        
        improvements = st.text_area("改善点・ご意見", placeholder="ご意見をお聞かせください")
        
        if st.button("アンケートを送信"):
            st.success("アンケートを送信しました。ご協力ありがとうございます！")
    
    with tab2:
        st.subheader("セッション別アンケート")
        
        session_name = st.selectbox("セッションを選択", [session["title"] for session in timetable if session["speaker"] != "-"])
        
        if session_name:
            session_satisfaction = st.slider("セッションの満足度", 1, 5, 3, key="session")
            session_comment = st.text_area("セッションについてのコメント", placeholder="セッションについてのご意見をお聞かせください")
            
            if st.button("セッションアンケートを送信"):
                st.success("セッションアンケートを送信しました。ご協力ありがとうございます！")

# チャットページ
elif selected == "💬 チャット":
    st.title("💬 チャット・交流")
    
    # チャット入力
    user_input = st.text_input("メッセージを入力", key="chat_input")
    
    if st.button("送信"):
        if user_input:
            st.session_state.chat_messages.append({
                "user": "あなた",
                "message": user_input,
                "time": datetime.now().strftime("%H:%M")
            })
            st.rerun()
    
    # チャット履歴表示
    st.subheader("チャット履歴")
    
    for message in st.session_state.chat_messages:
        st.markdown(f"""
        <div class="chat-message">
            <strong>{message['user']}</strong> ({message['time']})<br>
            {message['message']}
        </div>
        """, unsafe_allow_html=True)
    
    # サンプルメッセージ
    if not st.session_state.chat_messages:
        st.info("チャットを開始しましょう！他の参加者と交流できます。")

# 名刺交換ページ
elif selected == "📇 名刺交換":
    st.title("📇 名刺交換・連絡先共有")
    
    tab1, tab2 = st.tabs(["QRコード生成", "連絡先管理"])
    
    with tab1:
        st.subheader("QRコード生成")
        
        # 連絡先情報入力
        name = st.text_input("お名前")
        company = st.text_input("会社名")
        position = st.text_input("役職")
        email = st.text_input("メールアドレス")
        phone = st.text_input("電話番号")
        
        if st.button("QRコード生成"):
            if name and email:
                # QRコード生成
                contact_info = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nORG:{company}\nTITLE:{position}\nEMAIL:{email}\nTEL:{phone}\nEND:VCARD"
                
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(contact_info)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                
                # 画像をバイトに変換
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                st.image(img, caption="あなたの連絡先QRコード", width=200)
                
                # ダウンロードボタン
                st.download_button(
                    label="QRコードをダウンロード",
                    data=img_byte_arr,
                    file_name="contact_qr.png",
                    mime="image/png"
                )
    
    with tab2:
        st.subheader("連絡先管理")
        
        # 新しい連絡先追加
        with st.expander("新しい連絡先を追加"):
            new_name = st.text_input("お名前", key="new_name")
            new_company = st.text_input("会社名", key="new_company")
            new_email = st.text_input("メールアドレス", key="new_email")
            new_note = st.text_area("メモ", key="new_note")
            
            if st.button("連絡先を追加"):
                if new_name and new_email:
                    st.session_state.contacts.append({
                        "name": new_name,
                        "company": new_company,
                        "email": new_email,
                        "note": new_note,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("連絡先を追加しました！")
        
        # 連絡先一覧表示
        if st.session_state.contacts:
            st.subheader("保存された連絡先")
            for i, contact in enumerate(st.session_state.contacts):
                with st.expander(f"{contact['name']} - {contact['company']}"):
                    st.write(f"**メール:** {contact['email']}")
                    st.write(f"**メモ:** {contact['note']}")
                    st.write(f"**追加日時:** {contact['date']}")
                    
                    if st.button(f"削除", key=f"delete_{i}"):
                        st.session_state.contacts.pop(i)
                        st.rerun()
        else:
            st.info("まだ連絡先が保存されていません。")

# メモページ
elif selected == "📝 メモ":
    st.title("📝 メモ・ノート")
    
    # セッション選択
    session_options = [session["title"] for session in timetable if session["speaker"] != "-"]
    selected_session = st.selectbox("セッションを選択", ["全般"] + session_options)
    
    # メモ入力
    note_text = st.text_area(
        "メモを入力",
        value=st.session_state.notes.get(selected_session, ""),
        placeholder="セッションの内容や気づいたことをメモしてください..."
    )
    
    if st.button("メモを保存"):
        st.session_state.notes[selected_session] = note_text
        st.success("メモを保存しました！")
    
    # 保存されたメモ表示
    if st.session_state.notes:
        st.subheader("保存されたメモ")
        for session, note in st.session_state.notes.items():
            if note:  # 空でないメモのみ表示
                with st.expander(f"📝 {session}"):
                    st.write(note)
                    if st.button(f"削除", key=f"delete_note_{session}"):
                        st.session_state.notes[session] = ""
                        st.rerun()

# フッター
st.markdown("---")
st.markdown("© 2025 ノンプロ研 - すべての権利を留保します") 