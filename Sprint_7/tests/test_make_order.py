import requests
import allure
import pytest
import sys
import os
from urls import Url

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data import DataForOrder, StatusCode, TestData, ResponseBody, Flags


class TestOrderCreation:


    @pytest.mark.parametrize("color_data", [
        ["BLACK"], 
        ["GREY"], 
        ["BLACK", "GREY"]
    ])
    
    @allure.title('Создание заказа с цветами: {color_data}')
    def test_create_order_with_colors(self, color_data, create_test_order):
        order_data = DataForOrder.order_data.copy()
        order_data["color"] = color_data
        response, track_number = next(create_test_order(order_data))
        self._verify_successful_order_creation(response, track_number)

    @allure.title('Создание заказа с пустым массивом цветов')
    def test_create_order_with_empty_colors(self, create_test_order):
        order_data = DataForOrder.order_data.copy()
        order_data["color"] = []
        response, track_number = next(create_test_order(order_data))
        self._verify_successful_order_creation(response, track_number)

    @allure.title('Создание заказа без поля color')
    def test_create_order_without_color_field(self, create_test_order):
        order_data = DataForOrder.order_data.copy()
        del order_data["color"]
        response, track_number = next(create_test_order(order_data))    
        self._verify_successful_order_creation(response, track_number)

    def _verify_successful_order_creation(self, response, track_number):
        assert response.status_code == StatusCode.CREATED
        assert isinstance(response.json(), dict), "Ответ должен быть словарем"
        assert Flags.SUCCESSFUL_ORDER_CREATION in response.json(), "В ответе должно быть поле 'track'"
        assert isinstance(track_number, int), "Track номер должен быть числом"
        assert track_number > 0, "Track номер должен быть положительным"