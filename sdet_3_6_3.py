import json
import requests
import pytest
from faker import Faker
from constant import HEADERS, BASE_URL

@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session


fake = Faker()
def _generate_booking_data():
    # Generate two random dates
    date1 = fake.date_between(start_date='-1y', end_date='now')  # A random date in the last year
    date2 = fake.date_between(start_date='-1y', end_date='now')  # Another random date in the last year

    # Compare the two dates to find the earlier one
    earlier_date = date1 if date1 < date2 else date2
    later_date = date1 if date1 > date2 else date2

    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=10000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": f"{earlier_date}",
            "checkout": f"{later_date}"
        },
        "additionalneeds": f"{fake.words(nb=3, unique=True)}"
    }

@pytest.fixture()
def booking_data():
    return _generate_booking_data()


class TestBookings:

    @staticmethod
    def __created_booking_id(booking_data, auth_session):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID букинга не найден в ответе"
        return booking_id

    @staticmethod
    def __assert_response_booking_object(response_with_booking_data, booking_object):
        booking_data_response = response_with_booking_data.json()
        assert booking_data_response['firstname'] == booking_object['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_object['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_object['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_object['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_object['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_object['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

    def test_create_booking(self, booking_data, auth_session):
        booking_id = self.__created_booking_id(booking_data, auth_session)

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        self.__assert_response_booking_object(get_booking, booking_data)

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_replace_full_with_put(self, booking_data, auth_session):
        booking_id = self.__created_booking_id(booking_data, auth_session)

        #change all fields, replace all fields, assert
        new_booking_object = _generate_booking_data()
        updated_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=new_booking_object)

        self.__assert_response_booking_object(updated_booking, new_booking_object)

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"
        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_replace_part_with_put(self, booking_data, auth_session):
        booking_id = self.__created_booking_id(booking_data, auth_session)

        # change all fields, replace all fields, assert
        new_booking_object = _generate_booking_data()
        new_booking_object['firstname'] = booking_data['firstname']
        new_booking_object['lastname'] = booking_data['lastname']
        updated_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=new_booking_object)

        self.__assert_response_booking_object(updated_booking, new_booking_object)

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"
        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_replace_full_with_patch(self, booking_data, auth_session):
        booking_id = self.__created_booking_id(booking_data, auth_session)

        #change all fields, replace all fields, assert
        new_booking_object = _generate_booking_data()
        updated_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=new_booking_object)

        self.__assert_response_booking_object(updated_booking, new_booking_object)

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"
        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_replace_part_with_patch(self, booking_data, auth_session):
        booking_id = self.__created_booking_id(booking_data, auth_session)

        # change all fields, replace all fields, assert
        new_booking_object = _generate_booking_data()
        new_booking_object['firstname'] = booking_data['firstname']
        new_booking_object['lastname'] = booking_data['lastname']
        updated_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=new_booking_object)

        self.__assert_response_booking_object(updated_booking, new_booking_object)

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"
        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_get_all_bookings_id(self, auth_session):
        get_all_ids = auth_session.get(f"{BASE_URL}/booking/")
        assert get_all_ids.status_code == 200, f"Ошибка при получении ID для существующих бронирований"
        assert isinstance(get_all_ids.json(), list), "Ответ сервера не является списком"

        # Преобразуем ответ в JSON (ожидается, что это список)
        response_data = get_all_ids.json()

        # Проверяем, что каждый элемент списка является словарём и содержит ключ "bookingid"
        all_have_bookingid = all(isinstance(item, dict) and "bookingid" in item for item in response_data)

        # Утверждаем, что все элементы имеют ключ "bookingid"
        assert all_have_bookingid, "Не все элементы списка содержат ключ 'bookingid'"


    def test_get_bookings_with_filter(self, booking_data, auth_session):
        target_booking_id = self.__created_booking_id(booking_data, auth_session)
        filters = f"?firstname={booking_data['firstname']}"
        get_all_filtered_ids = auth_session.get(f"{BASE_URL}/booking{filters}")
        assert get_all_filtered_ids.status_code == 200, \
            f"Ошибка при получении ID для существующих бронирований с фильтрацией"

        response_data = get_all_filtered_ids.json()
        all_have_bookingid = all(isinstance(item, dict) and "bookingid" in item for item in response_data)
        assert all_have_bookingid, "Не все элементы списка содержат ключ 'bookingid'"

        # Проверяем, есть ли объект с таким bookingid
        exists = any(item.get('bookingid') == target_booking_id for item in response_data)

        # Утверждаем, что объект существует
        assert exists, f"Объект с bookingid {target_booking_id} не найден при использовании get с фильтрацией по имени"


    def test_get_bookings_with_two_filters(self, booking_data, auth_session):
        # Создадим три бронирования и запишем их bookingid в лист
        target_bookings_id = [
            self.__created_booking_id(booking_data, auth_session)
            for _ in range(3)
        ]

        filters = f"?firstname={booking_data['firstname']}&lastname={booking_data['lastname']}"
        get_all_filtered_ids = auth_session.get(f"{BASE_URL}/booking{filters}")
        assert get_all_filtered_ids.status_code == 200, \
            f"Ошибка при получении ID для существующих бронирований с фильтрацией"

        response_data = get_all_filtered_ids.json()
        all_have_bookingid = all(isinstance(item, dict) and "bookingid" in item for item in response_data)
        assert all_have_bookingid, "Не все элементы списка содержат ключ 'bookingid'"

        # Проверяем, что все созданные объекты есть в списке после фильтрации
        for target_id in target_bookings_id:
            exists = any(item.get('bookingid') == target_id for item in response_data)
            assert exists, \
                f"Объект с bookingid {target_id} не найден при использовании get с фильтрацией по имени и фамилии"


"""
# TODO:

Покрыть тестами методы put, patch, get (общий, без id).
Кейсы нужно будет придумать самостоятельно, исходя из бизнес-логики приложения.
В итоге должно получиться 7-10 тестов, но можно и больше.
"""