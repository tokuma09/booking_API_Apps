from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
# ユーザー一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # skipで最初の何行スキップするかを指定
    # limitで取得する数を指定
    return db.query(models.User).offset(skip).limit(limit).all()

# 会議室一覧取得
def get_rooms(db: Session, skip: int =0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()


# 予約一覧取得
def get_bookings(db: Session, skip: int=0, limit: int =100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


# ユーザー登録
def create_user(db: Session, user: schemas.User):
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 会議室登録
def create_room(db: Session, room: schemas.Room):
    db_room = models.Room(room_name=room.room_name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


# 予約登録
def create_booking(db: Session, booking: schemas.Booking):

    # 飛んできた予約情報と重複している予約情報を取得
    # 重複しているとは、同じ会議室で同じ時間帯に予約が入っていること
    # (予約開始時間が既存の予約の終了時間よりも前で、予約終了時間が既存の予約の開始時間よりも後)
    db_booked = db.query(models.Booking).filter(models.Booking.room_id == booking.room_id).\
        filter(booking.start_datetime < models.Booking.end_datetime).\
        filter(models.Booking.start_datetime < booking.end_datetime).all()

    if len(db_booked) ==0:
        # 重複しないのであれば、登録
        db_booking = models.Booking(user_id=booking.user_id,
                                    room_id=booking.room_id,
                                    booking_num=booking.booking_num,
                                    start_datetime=booking.start_datetime,
                                    end_datetime=booking.end_datetime)
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
    else:
        raise HTTPException(status_code=404, detail="予約が重複しています")

    return db_booking

