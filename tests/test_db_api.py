import json
import requests

url = "http://10.0.0.238:8888"

get_slide_data = {
    "slideid": "KL20-12031_B_2.35.1",
    "blockid": "KL20-12031_B_2",
    "accessionid": "KL20-12031",
    "stain": "H&E",
    "stainorderdate": "2020-09-08 15:22:36",
    "sitelabel": "MAWD",
    "casetype": "KL",
    "year": "20",
    "ts": "1624179320.740725",
    "location": "5",
    "retrievalrequest": None,
    "requestedby": None,
    "requestts": None,
    "box_id": "Box1",
}

def test_get_slide():
    get_slide_url = url + "/get_slide"

    response = requests.post(
        get_slide_url, json={"payload": "KL20-12031_B_2.35.1"}
    )

    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data == get_slide_data


if __name__ == "__main__":
    test_get_slide()
