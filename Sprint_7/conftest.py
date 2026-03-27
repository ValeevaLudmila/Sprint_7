import pytest
import requests
import generators
from urls import Url
from data import DataForOrder, Flags
import time
import random


@pytest.fixture
def create_order():
    # Фикстура для создания заказа с автоматической отменой после теста
    order_response = requests.post(f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', json=DataForOrder.ORDER_DATA_FOR_TRACK_TEST)
    order_track = order_response.json()["track"]
    yield order_track
    requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', params={"track": order_track})


@pytest.fixture
def create_order_with_id():
    # Фикстура для создания заказа с возвратом track и ID
    order_response = requests.post(f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', json=DataForOrder.ORDER_DATA_FOR_TRACK_TEST)
    order_track = order_response.json()["track"]
    order_id = requests.get(f'{Url.MAIN_URL}{Url.Get_ORDER_BY_NUMBER}?t={order_track}').json().get("order", {}).get("id")
    yield order_track, order_id
    requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', params={"track": order_track})

@pytest.fixture
def create_test_order():
    # Фикстура для создания тестового заказа с автоматической отменой
    def _create_order(order_data):
        response = requests.post(f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', json=order_data)
        track_number = response.json()[Flags.SUCCESSFUL_ORDER_CREATION]
        yield response, track_number
        requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', json={"track": track_number})
    return _create_order

@pytest.fixture
def create_order_for_accept_test():
    # Фикстура для создания заказа специально для тестов принятия заказа
    order_response = requests.post(f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', json=DataForOrder.VALID_ORDER_DATA_2)
    order_track = order_response.json()["track"]
    order_id = requests.get(f'{Url.MAIN_URL}{Url.Get_ORDER_BY_NUMBER}?t={order_track}').json().get("order", {}).get("id")
    yield order_track, order_id
    requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', params={"track": order_track})


@pytest.fixture
def create_courier():
    name = generators.name_generator()
    login = generators.login_generator()
    password = generators.password_generator()
    create_courier_body = {'login': login, 'password': password, 'firstName': name}
    login_courier_body = {'login': login, 'password': password}
    requests.post(f'{Url.MAIN_URL}{Url.CREATING_COURIER}', json=create_courier_body)
    login_courier = requests.post(f'{Url.MAIN_URL}{Url.COURIER_LOGIN}', json=login_courier_body)
    courier_id = login_courier.json()["id"]
    yield [create_courier_body, login_courier_body, login, password, courier_id]
    requests.delete(f'{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}')


@pytest.fixture
def generate_courier_data():
    name = generators.name_generator()
    # Добавляем уникальность к логину
    timestamp = str(int(time.time() * 1000))[-6:]
    random_num = str(random.randint(100, 999))
    login = generators.login_generator() + timestamp + random_num
    password = generators.password_generator()
    creation_courier_body = {'login': login, 'password': password, 'firstName': name}
    login_courier_body = {'login': login, 'password': password}
    yield [creation_courier_body, login_courier_body]
    try:
        login_courier = requests.post(f'{Url.MAIN_URL}{Url.COURIER_LOGIN}', json=login_courier_body)
        if login_courier.status_code == 200 and 'id' in login_courier.json():
            requests.delete(f'{Url.MAIN_URL}{Url.COURIER_DELETE}{login_courier.json()["id"]}')
    except Exception as e:
        print(f"Ошибка при очистке курьера: {e}")