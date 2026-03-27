import requests
import allure
import pytest
import sys
import os
from urls import Url

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data import DataForOrder, StatusCode, TestData, ResponseBody, Flags
from generators import login_generator, password_generator, name_generator

class TestDeleteCourier:
    
    @allure.title('Успешное удаление курьера')
    def test_delete_courier(self, create_courier):
        with allure.step("Логин курьера для получения ID"):
            login_response = requests.post(
                f'{Url.MAIN_URL}{Url.COURIER_LOGIN}', 
                json=create_courier[1]
            )
        courier_id = login_response.json()["id"]
        with allure.step("Удалить курьера по ID"):
            response = requests.delete(f'{Url.MAIN_URL}{Url.COURIER_DELETE}{courier_id}')
        assert response.status_code == StatusCode.OK and response.json() == TestData.SUCCESS_DELETE_RESPONSE

    @allure.title('Ошибка при запросе с несуществующим id')  # Баг: 500 вместо 404
    @pytest.mark.skip(reason="BUG: Server returns 500 instead of 404 for nonexistent courier")
    def test_delete_nonexistent_courier_returns_error(self):
        with allure.step("Попытка удаления несуществующего курьера"):
            response = requests.delete(f'{Url.MAIN_URL}{Url.COURIER_DELETE}{TestData.NONEXISTENT_COURIER_ID}')
        assert response.status_code == StatusCode.NOT_FOUND and response.json() == ResponseBody.COURIER_ACCOUNT_NOT_FOUND

    @allure.title('Ошибка при запросе без id') # Баг: 404 вместо 400
    @pytest.mark.skip(reason="BUG: Server returns 404 instead of 400 when courier ID is missing")
    def test_delete_courier_without_id_returns_error(self):
        with allure.step("Попытка удаления курьера без ID"):
            response = requests.delete(f'{Url.MAIN_URL}{Url.COURIER_DELETE}')
        assert response.status_code == StatusCode.BAD_REQUEST and "message" in response.json()