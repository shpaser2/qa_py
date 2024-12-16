import json

"""
To see the report execute one of the next commands:
git    python test_sdet_3_6_1.py
    pytest -s test_sdet_3_6_1.py
"""


class Operator:
    @staticmethod
    def get_name_email():
        NAME_AND_EMAIL = "Sergei, example@google.com"
        return NAME_AND_EMAIL

data = {
    "state": 0,
    "data": [
        {
            "_id": "3d8c861f-e2c0-442a-9d82-810ae5eb5f52",
            "count": 1,
            "brand_id": 84375,
            "delay": 1,
            "startedAt": "2024-03-21T16:48:03.513Z",
            "completedAt": "2024-03-21T16:48:03.513Z",
            "completed": 0,
            "wait_refund": 0,
            "refunded": 0
        },
        {
            "_id": "4816385b-a5a5-4341-aedf-6f80bedbdce4",
            "count": 2,
            "brand_id": 88339,
            "delay": 2,
            "startedAt": "2024-03-21T16:27:32.062Z",
            "completedAt": "2024-03-21T16:28:32.062Z",
            "completed": 0,
            "wait_refund": 2,
            "refunded": 0
        },
        {
            "_id": "7e0882b5-38b8-4dcb-9825-625158a92314",
            "count": 16,
            "brand_id": 88339,
            "delay": 3,
            "startedAt": "2024-03-21T16:17:04.723Z",
            "completedAt": "2024-03-21T16:17:04.723Z",
            "completed": 7,
            "wait_refund": 3,
            "refunded": 6
        }
    ]
}


SPECIAL_REPORT_ID = "326b23a1-e6ab-4b4a-84a1-a3ecb33afc97"
report = {
    "orders_id":[],
    "services_overall":{"completed": 0, "refunded": 0, "wait_refund": 0},
    "operator_info":""
}

def prepare_report(d = data, r = report):
    for order in d["data"]:
        r["orders_id"].append(order["_id"])
        r["services_overall"]["completed"] += order["completed"]
        r["services_overall"]["refunded"] +=  order["refunded"]
        r["services_overall"]["wait_refund"] += order["wait_refund"]
    r["orders_id"].append(SPECIAL_REPORT_ID)
    r["operator_info"] = Operator.get_name_email()
    return r

def print_report(r):
    print("\n\nReport:")
    # simple, less readable
    # for key, value in r.items():
    #     print(f"{key}: {value}")
    # print("\n")
    #well readable
    print(json.dumps(r, indent=4))

print_report(prepare_report())


def test_data_is_present():
    assert len(data["data"]) > 0

def test_exec_time_1st_and_2nd_less_6hours():
    delay_between_orders = 2 #hours
    def get_waiting_orders(order_number):
        return (data["data"][order_number]["count"] -
                data["data"][order_number]["completed"])
    orders = get_waiting_orders(0) + get_waiting_orders(1)
    exec_time = 2 * (orders - 1) #summary of delays between orders
    assert exec_time < 6

def test_check_3rd_order():
    assert (
        (data["data"][2]["count"] == (data["data"][2]["completed"] +
                                    data["data"][2]["wait_refund"] +
                                    data["data"][2]["refunded"]) and
        data["data"][2]["completed"] >= data["data"][2]["count"] / 2
        ) or
        (data["data"][2]["refunded"] <= data["data"][2]["completed"] and
         data["data"][2]["wait_refund"] <= data["data"][2]["refunded"]
        )
    )

