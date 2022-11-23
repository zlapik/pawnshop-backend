import datetime

import pytest
from statistic.models import StatisticDescription, StatisticQPData
from rest_framework import status

statistic_urls = {key: f"/statistic/?data={key}" for key in StatisticQPData.names if key != StatisticQPData.RESET.name}
statistic_urls[StatisticQPData.RESET.name] = "/statistic/"


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "user": 1,
                "status": "LOAN",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Praha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "3.0",
                "inventory_id": 3,
                "product_name": "prod1",
                "buy_price": 11000,
                "sell_price": 11330,
            },
        ),
    ],
)
@pytest.mark.django_db
def test_loan_create(client_admin, load_all_fixtures_for_module, payload):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.post(path="/product/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] - product["buy_price"]
    assert new_stat["profit"] == old_stat["profit"] - product["buy_price"]
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.LOAN_CREATE.label
    assert new_stat["price"] == -product["buy_price"]
    assert new_stat["product"] == response_update.data["id"]


@pytest.mark.parametrize(
    "product_id, payload",
    [
        pytest.param(
            6,
            {"update": StatisticDescription.LOAN_TO_OFFER.name, "sell_price": 1200},
        ),
    ],
)
@pytest.mark.django_db
def test_loan_to_offer(client_admin, load_all_fixtures_for_function, product_id, payload):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"]
    assert new_stat["profit"] == old_stat["profit"]
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.LOAN_TO_OFFER.label
    assert new_stat["price"] == 0
    assert new_stat["product"] == response_update.data["id"]


@pytest.mark.parametrize(
    "product_id, payload",
    [
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_EXTEND.name},
        ),
        # pytest.param(6, {"update": StatisticDescription.LOAN_TO_OFFER.label, "sell_price": 1200}, ),
    ],
)
@pytest.mark.django_db
def test_loan_extend(client_admin, load_all_fixtures_for_function, product_id, payload):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] + (product["sell_price"] - product["buy_price"])
    assert new_stat["profit"] == old_stat["profit"] + (product["sell_price"] - product["buy_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.LOAN_EXTEND.label
    assert new_stat["price"] == (product["sell_price"] - product["buy_price"])
    assert new_stat["product"] == response_update.data["id"]


@pytest.mark.parametrize(
    "product_id, payload",
    [
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_RETURN.name},
        ),
    ],
)
@pytest.mark.django_db
def test_loan_return(client_admin, load_all_fixtures_for_function, product_id, payload):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] + product["sell_price"]
    assert new_stat["profit"] == old_stat["profit"] + product["sell_price"]
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.LOAN_RETURN.label
    assert new_stat["price"] == product["sell_price"]
    assert new_stat["product"] == response_update.data["id"]


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "user": 1,
                "status": "OFFER",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Prha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "1.0",
                "inventory_id": 3,
                "product_name": "prod1",
                "buy_price": 100,
                "sell_price": 200,
            },
        ),
    ],
)
@pytest.mark.django_db
def test_offer_create(client_admin, load_all_fixtures_for_function, payload):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.post(path="/product/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] - product["buy_price"]
    assert new_stat["profit"] == old_stat["profit"] - product["buy_price"]
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_BUY.label
    assert new_stat["price"] == -product["buy_price"]
    assert new_stat["product"] == response_update.data["id"]


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 1,
            },
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 2,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_buy(client_admin, load_all_fixtures_for_function, product_id, payload, exp_status):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] - (payload["quantity"] * product["buy_price"])
    assert new_stat["profit"] == old_stat["profit"] - (payload["quantity"] * product["buy_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_BUY.label
    assert new_stat["price"] == -product["buy_price"] * payload["quantity"]
    assert new_stat["product"] == product_id


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.OFFER_SELL.name}",
                "quantity": 1,
            },
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {
                "update": f"{StatisticDescription.OFFER_SELL.name}",
                "quantity": 2,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_sell(client_admin, load_all_fixtures_for_function, product_id, payload, exp_status):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["description"] == StatisticDescription.OFFER_SELL.label
    assert new_stat["amount"] == old_stat["amount"] + (payload["quantity"] * product["sell_price"])
    assert new_stat["profit"] == old_stat["profit"] + (payload["quantity"] * product["sell_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_SELL.label
    assert new_stat["price"] == product["sell_price"] * payload["quantity"]
    assert new_stat["product"] == product_id


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.UPDATE_DATA.name}",
                "product_name": "Telefon Samsung 1",
                "sell_price": 100,
                "date_create": "2022-09-01T14:31:47.080000Z",
                "date_extend": "2022-09-01T14:31:47.080000Z",
                "inventory_id": 23,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_update_not_in_db(client_admin, load_all_fixtures_for_function, product_id, payload, exp_status):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    response_get_2 = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])

    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data)
    assert new_stat["amount"] == old_stat["amount"]
    assert new_stat["profit"] == old_stat["profit"]
    assert new_stat["datetime"] == old_stat["datetime"]
    assert new_stat["description"] == old_stat["description"]
    assert new_stat["price"] == old_stat["price"]
    assert new_stat["product"] == old_stat["product"]


# Data
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
def test_statistic_all_data(client_admin, load_all_fixtures_for_function):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    assert len(response_get.data) == 18


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
def test_statistic_cash_amount_data(client_admin, load_all_fixtures_for_function):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.CASH_AMOUNT.name])
    response_get_all = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    assert len(response_get.data) == 1
    assert response_get.data[0]["amount"] == response_get_all.data[-1]["amount"]


@pytest.mark.parametrize(
    "exp_data",
    [
        pytest.param(
            [
                {
                    "date": "2022-10-03",
                    "loan_create_count": 1,
                    "loan_extend_count": 1,
                    "loan_return_count": 1,
                    "loan_income": 140,
                    "loan_outcome": -100,
                    "loan_profit": 40,
                    "offer_create_count": 0,
                    "offer_sell_count": 1,
                    "offer_income": None,
                    "offer_outcome": 120,
                    "offer_profit": 120,
                    "all_income": 260,
                    "all_outcome": 120,
                    "all_profit": 160,
                },
                {
                    "date": "2022-10-04",
                    "loan_create_count": 2,
                    "loan_extend_count": 1,
                    "loan_return_count": 1,
                    "loan_income": 140,
                    "loan_outcome": -200,
                    "loan_profit": -60,
                    "offer_create_count": 0,
                    "offer_sell_count": 1,
                    "offer_income": None,
                    "offer_outcome": 120,
                    "offer_profit": 120,
                    "all_income": 260,
                    "all_outcome": 120,
                    "all_profit": 60,
                },
            ]
        )
    ],
)
@pytest.mark.django_db
def test_statistic_daily_stats_data(client_admin, load_all_fixtures_for_function, exp_data):
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.DAILY_STATS.name])
    assert len(response_get.data) == 2
    assert response_get.data == exp_data


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        pytest.param({"update": f"{StatisticDescription.RESET.name}"}, status.HTTP_201_CREATED),
    ],
)
@pytest.mark.django_db
def test_statistic_reset_profit(client_admin, load_all_fixtures_for_module, payload, exp_status):
    response = client_admin.post(path=statistic_urls[StatisticQPData.RESET.name], data=payload, format="json")
    response_get = client_admin.get(path=statistic_urls[StatisticQPData.ALL.name])
    assert response.status_code == exp_status
    assert len(response_get.data) == 19
    assert response_get.data[-1]["description"] == StatisticDescription.RESET.label
    assert response_get.data[-1]["profit"] == 0


@pytest.mark.skip("Not implemented")
def test_user_login():
    pass


@pytest.mark.skip("Not implemented")
def test_user_logout():
    pass


@pytest.mark.skip("Not implemented")
def test_user_created():
    pass


@pytest.mark.skip("Not implemented")
def test_user_deleted():
    pass


@pytest.mark.skip("Not implemented")
def test_user_updated():
    pass
