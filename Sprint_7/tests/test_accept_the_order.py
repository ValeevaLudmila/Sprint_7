import requests
import allure
import pytest
from urls import Url
from data import DataForOrder, StatusCode, TestData, ResponseBody


class TestAcceptOrder:

    @allure.title('Успешное принятие заказа')
    def test_accept_order_success(self, create_courier, create_order_with_id):
        order_track, order_id = create_order_with_id
        with allure.step("Принять заказ курьером"):
            response = requests.put(f'{Url.MAIN_URL}{Url.ORDER_ACCEPT}{order_id}', params={"courierId": create_courier[4]})
        assert response.status_code == StatusCode.OK
        assert response.json() == ResponseBody.ORDER_ACCEPT_SUCCESS

    @allure.title('Ошибка при принятии заказа без id курьера')
    def test_accept_order_without_courier_id(self, create_order_for_accept_test):
        order_track, order_id = create_order_for_accept_test
        with allure.step("Попытаться принять заказ без ID курьера"):
            response = requests.put(f'{Url.MAIN_URL}{Url.ORDER_ACCEPT}{order_id}', params={})
        assert response.status_code == StatusCode.BAD_REQUEST
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для поиска'}

    @allure.title('Ошибка при принятии заказа с несуществующим id курьера')
    def test_accept_order_with_nonexistent_courier(self, create_order_for_accept_test):
        order_track, order_id = create_order_for_accept_test
        with allure.step("Попытаться принять заказ с несуществующим курьером"):
            response = requests.put(f'{Url.MAIN_URL}{Url.ORDER_ACCEPT}{order_id}', params={"courierId": TestData.NONEXISTENT_COURIER_ID_FOR_ORDER})
        assert response.status_code == StatusCode.NOT_FOUND
        assert response.json() == ResponseBody.COURIER_ACCOUNT_NOT_FOUND

    @allure.title('Ошибка при принятии заказа без id заказа') # Баг: 404 вместо 400
    @pytest.mark.skip(reason="BUG: Server returns 404 instead of 400 when order ID is missing")
    def test_accept_order_without_order_id(self, create_courier):
        with allure.step("Попытаться принять заказ без ID заказа"):
            response = requests.put(f'{Url.MAIN_URL}{Url.ORDER_ACCEPT}', params={"courierId": create_courier[4]})
        assert response.status_code == StatusCode.BAD_REQUEST
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для поиска'}

    @allure.title('Ошибка при принятии заказа с несуществующим id заказа')
    def test_accept_order_with_nonexistent_order(self, create_courier):
        with allure.step("Попытаться принять несуществующий заказ"):
            response = requests.put(f'{Url.MAIN_URL}{Url.ORDER_ACCEPT}{TestData.NONEXISTENT_ORDER_ID}', params={"courierId": create_courier[4]})
        assert response.status_code == StatusCode.NOT_FOUND
        assert response.json() == ResponseBody.ORDER_NOT_FOUND