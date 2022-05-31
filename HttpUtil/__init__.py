import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


def get(url: str, params: dict = None) -> str:
    print(url)
    response = requests.get(url, params=params, headers=headers)
    response.encoding = 'gbk'
    if response.status_code == 200:
        return str(response.text)
