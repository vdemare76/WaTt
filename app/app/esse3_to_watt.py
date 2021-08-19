import requests, base64

url = "https://uniparthenope.esse3.cineca.it/e3rest/api/"
headers = {
    'Content-Type': "application/json",
    "Authorization": "Basic " + "MDEwODAwMTY3MjoyMkxlb24wOQ=="
}

response = requests.request("GET", url + "login", headers=headers, timeout=60)
            r = response.json()
            token = r["authToken"]
            message_bytes = token.encode('utf-8')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('utf-8')

            headers = {
                'Content-Type': "application/json",
                "Authorization": "Basic " + base64_message
            }
            response = requests.request("GET", url + "offerta-service-v1/offerte?aaOffId=2020", headers=headers, timeout=60)
            flash(response.json())