import requests
import allure
import pytest
import sys
import os
from urls import Url

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data import DataForOrder, StatusCode, TestData, ResponseBody, Flags


class TestGetOrdersList:

    @allure.title('Получение списка заказов')
    def test_orders_list_returns_array(self):
        with allure.step("Создать тестовый заказ"):
            order_response = requests.post(
                f'{Url.MAIN_URL}{Url.POST_CREATING_ORDER}', 
                json=DataForOrder.VALID_ORDER_DATA_1
            )
            assert order_response.status_code == StatusCode.CREATED
            track_number = order_response.json()[Flags.SUCCESSFUL_ORDER_CREATION]

        try:
            with allure.step("Получить список заказов"):
                response = requests.get(f'{Url.MAIN_URL}{Url.GET_ORDER_LIST}')
            
            assert response.status_code == StatusCode.OK
            assert Flags.SUCCESSFUL_GET_ORDER_LIST in response.json()
            orders = response.json()[Flags.SUCCESSFUL_GET_ORDER_LIST]
            assert isinstance(orders, list)
            assert len(orders) > 0, "Список заказов не должен быть пустым после создания тестового заказа"
            
            first_order = orders[0]
            required_fields = ["id", "track", "firstName", "lastName", "address"]
            for field in required_fields:
                assert field in first_order, f"В заказе должно быть поле {field}"
            
        finally:
            requests.put(f'{Url.MAIN_URL}{Url.ORDER_CANCEL}', json={"track": track_number})