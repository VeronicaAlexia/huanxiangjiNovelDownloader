import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


def get(url: str, params: dict = None, max_retry: int = 5) -> str:
    for retry in range(max_retry):
        try:
            response = requests.get(url, params=params, headers=headers)
            response.encoding = 'gbk'
            if response.status_code == 200:
                return str(response.text)
        except Exception as error:
            print("Get retry: {} error:{}".format(retry, error))
