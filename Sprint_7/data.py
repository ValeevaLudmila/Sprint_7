import generators


class StatusCode:
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409
    OK = 200
    GATEWAY_TIMEOUT = 504


class TestData:
    NONEXISTENT_COURIER_ID = 9999999999999999999999
    SUCCESS_DELETE_RESPONSE = {"ok": True}
    NONEXISTENT_ORDER_ID = 999999
    NONEXISTENT_COURIER_ID_FOR_ORDER = 999999
    NONEXISTENT_TRACK_NUMBER = 999999
    NONEXISTENT_USER_LOGIN = "nonexistent_user_12345"
    INVALID_USER_PASSWORD = "invalid_password_12345"


class DataForOrder:
    VALID_ORDER_DATA_1 = {
        "firstName": "Иван",
        "lastName": "Ульянов", 
        "address": "Борисоглебская",
        "metroStation": 7,
        "phone": "+7 904 356 47 53",
        "rentTime": 1,
        "deliveryDate": "2025-09-27",
        "comment": "тест",
        "color": ["BLACK"]
    }
    
    VALID_ORDER_DATA_2 = {
        "firstName": "Тест",
        "lastName": "Тестов", 
        "address": "Адрес",
        "metroStation": 4,
        "phone": "+7 800 355 35 35", 
        "rentTime": 1,
        "deliveryDate": "2025-01-01",
        "comment": "тест",
        "color": ["BLACK"]
    }
    
    ORDER_DATA_FOR_TRACK_TEST = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Адрес",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 1,
        "deliveryDate": "2025-01-01",
        "comment": "тест",
        "color": ["BLACK"]
    }
    
    order_data = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    
    ACCEPT_ORDER_TEST_PARAMS = [
        ("без id курьера", "real", "", StatusCode.BAD_REQUEST),
        ("с несуществующим id курьера", "real", TestData.NONEXISTENT_COURIER_ID_FOR_ORDER, StatusCode.NOT_FOUND),
        ("без id заказа", "", "real", StatusCode.BAD_REQUEST),
        ("с несуществующим id заказа", TestData.NONEXISTENT_ORDER_ID, "real", StatusCode.NOT_FOUND),
    ]
    
    COLOR_TEST_PARAMS = [
        ["BLACK"], 
        ["GREY"], 
        ["BLACK", "GREY"], 
        [], 
        None
    ]


class DataForRegistration:
    reg_data = [
        {'login': generators.login_generator(), 'firstName': generators.name_generator(), 'password': generators.password_generator()},
    ]


class ResponseBody:
    # Успешные ответы
    COURIER_CREATION_SUCCESS = {'ok': True}
    ORDER_ACCEPT_SUCCESS = {'ok': True}
    
    # Ошибки курьеров
    COURIER_NAME_ALREADY_EXIST = {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}
    COURIER_REGISTRATION_NOT_ENOUGH_DATA = {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}
    COURIER_LOGIN_NOT_ENOUGH_DATA = {'code': 400, 'message': 'Недостаточно данных для входа'}
    COURIER_LOGIN_NOT_FOUND = {"code": 404, "message": "Учетная запись не найдена"}
    COURIER_ACCOUNT_NOT_FOUND = {"code": 404, "message": "Курьера с таким id не существует"}
    
    # Ошибки заказов
    ORDER_NOT_FOUND = {"code": 404, "message": "Заказа с таким id не существует"}
    ORDER_BY_TRACK_NOT_FOUND = {"code": 404, "message": "Заказ не найден"}
    ORDER_TRACK_MISSING = {'code': 400, 'message': 'Недостаточно данных для поиска'}


class Flags:
    SUCCESSFUL_ORDER_CREATION = 'track'
    SUCCESSFUL_GET_ORDER_LIST = 'orders'
    ORDER_IN_RESPONSE = 'order'
    COURIER_ID_IN_RESPONSE = 'id'