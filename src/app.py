import streamlit as st
import random
import requests
import datetime


page = st.sidebar.selectbox("APIテスト画面", ["users", "rooms", "bookings"])
if page == "users":
    st.title('APIテスト画面(ユーザー)')

    # フォームに乗せる情報はここ
    with st.form(key='user'):
        user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザー名', max_chars=12)

        data = {
            "user_id": user_id,
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write("## レスポンス結果")
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())

elif page == "rooms":
    st.title('APIテスト画面(会議室)')

    # フォームに乗せる情報はここ
    with st.form(key='room'):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write("## レスポンス結果")
        url = 'http://127.0.0.1:8000/rooms'
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())
elif page == "bookings":
    st.title('APIテスト画面(予約)')

    # フォームに乗せる情報はここ
    with st.form(key='room'):
        booking_id: int = random.randint(0, 10)
        user_id: int = random.randint(0, 10)
        room_id: int = random.randint(0, 10)
        booking_num: int = st.number_input('予約人数', step=1)

        start_date = st.date_input('予約日時を設定', min_value=datetime.datetime.today(), key="start_date")
        start_time = st.time_input('予約開始時間を設定', value=datetime.time(9, 00))
        start_datetime = datetime.datetime.combine(start_date, start_time).isoformat()

        end_date = st.date_input('予約日時を設定', min_value=datetime.datetime.today(), key="end_date")
        end_time = st.time_input('予約終了時間を設定', value=datetime.time(18, 00))
        end_datetime = datetime.datetime.combine(end_date, end_time).isoformat()

        data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "booking_num": booking_num,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }
        submit_button = st.form_submit_button(label='リクエスト送信')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        st.write('## 送信データ')
        st.json(data)
        st.write("## レスポンス結果")
        url = 'http://127.0.0.1:8000/bookings'
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())
