import requests
import allure
from urls import Url
from data import DataForOrder, StatusCode, TestData, ResponseBody, Flags


class TestGetOrderByTrack:

    @allure.title('Успешное получение заказа')
    def test_get_order_success(self):
        with allure.step("Создать заказ"):
            order_response = requests.post(f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', json=DataForOrder.ORDER_DATA_FOR_TRACK_TEST)
        track = order_response.json()["track"]
        with allure.step("Получить заказ по треку"):
            response = requests.get(f'{Url.MAIN_URL}{Url.Get_ORDER_BY_NUMBER}?t={track}')
        assert response.status_code == StatusCode.OK and Flags.ORDER_IN_RESPONSE in response.json()
        with allure.step("Отменить заказ"):
            requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', params={"track": track})

    @allure.title('Ошибка при отсутствии номера')
    def test_get_order_without_track(self):
        with allure.step("Запрос заказа без номера трека"):
            response = requests.get(f'{Url.MAIN_URL}{Url.Get_ORDER_BY_NUMBER}')
        assert response.status_code == StatusCode.BAD_REQUEST and response.json() == ResponseBody.ORDER_TRACK_MISSING

    @allure.title('Ошибка при несуществующем номере')
    def test_get_order_nonexistent_track(self):
        with allure.step("Запрос заказа с несуществующим треком"):
            response = requests.get(f'{Url.MAIN_URL}{Url.Get_ORDER_BY_NUMBER}?t={TestData.NONEXISTENT_TRACK_NUMBER}')
        assert response.status_code == StatusCode.NOT_FOUND
        assert response.json() == ResponseBody.ORDER_BY_TRACK_NOT_FOUND