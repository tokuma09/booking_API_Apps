import streamlit as st
import random
import requests
import datetime
import pandas as pd

page = st.sidebar.selectbox("APIテスト画面", ["users", "rooms", "bookings"])
if page == "users":
    st.title('ユーザー登録画面')

    # フォームに乗せる情報はここ
    with st.form(key='user'):
        # user_id: int = random.randint(0, 10)
        user_name: str = st.text_input('ユーザー名', max_chars=12)

        data = {
            # "user_id": user_id,
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label='ユーザー登録')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(url, json=data)

        if res.status_code ==200:
            st.success('ユーザー登録完了')
        else:
            st.write(f"Error: {res.status_code}")

        st.json(res.json())

elif page == "rooms":
    st.title('会議室登録画面')

    # フォームに乗せる情報はここ
    with st.form(key='room'):
        #room_id: int = random.randint(0, 10)
        room_name: str = st.text_input('会議室名', max_chars=12)
        capacity: int = st.number_input('定員', step=1)
        data = {
            #"room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label='会議室登録')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        url = 'http://127.0.0.1:8000/rooms'
        res = requests.post(url, json=data)

        if res.status_code == 200:
            st.success('会議室登録完了')
        else:
            st.write(f"Error: {res.status_code}")
        st.json(res.json())

elif page == "bookings":
    st.title('会議室予約画面')

    # ユーザー一覧を取得
    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()
    users_dict = {user['user_name']: user['user_id'] for user in users}

    # 会議室一覧を取得
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_dict = {
        room['room_name']: {"room_id": room['room_id'], "capacity":room['capacity']} for room in rooms}

    st.write("### 会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    st.write("### 予約一覧")
    url_bookings = "http://127.0.0.1:8000/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)
    st.table(df_bookings)

    # フォームに乗せる情報はここ
    with st.form(key='room'):
        # booking_id: int = random.randint(0, 10)
        user_name : str = st.selectbox('ユーザー名', list(users_dict.keys()))
        room_name: str = st.selectbox('会議室名', list(rooms_dict.keys()))

        booking_num: int = st.number_input('予約人数', step=1, min_value=1)

        start_date = st.date_input('予約日時を設定', min_value=datetime.datetime.today(), key="start_date")
        start_time = st.time_input('予約開始時間を設定', value=datetime.time(9, 00))
        start_datetime = datetime.datetime.combine(start_date, start_time).isoformat()

        end_date = st.date_input('予約日時を設定', min_value=datetime.datetime.today(), key="end_date")
        end_time = st.time_input('予約終了時間を設定', value=datetime.time(18, 00))
        end_datetime = datetime.datetime.combine(end_date, end_time).isoformat()

        # data = {
        #     "booking_id": booking_id,
        #     "user_id": user_id,
        #     "room_id": room_id,
        #     "booking_num": booking_num,
        #     "start_datetime": start_datetime,
        #     "end_datetime": end_datetime
        # }
        submit_button = st.form_submit_button(label='リクエスト送信')

    # フォームが送信されたらFastAPIで作ったAPIサーバーにリクエストをおくる
    if submit_button:
        user_id = users_dict[user_name]
        room_id = rooms_dict[room_name]['room_id']
        capacity = rooms_dict[room_name]['capacity']
        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booking_num": booking_num,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }
        if booking_num <= capacity:

            url = 'http://127.0.0.1:8000/bookings'
            res = requests.post(url, json=data)
            if res.status_code == 200:
                st.success('予約登録完了')
            st.json(res.json())
        else:
            st.error('定員オーバーです。')
            st.write(f"定員: {capacity}人, 予約人数: {booking_num}人 {capacity-booking_num}人オーバーです。")
