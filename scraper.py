import requests
from typing import List, Dict, Any

EXCLUDE_KEYWORDS = ["식품", "음료", "기계", "공구", "전자제품", "의류", "신발", "옷", "냉장고", "세탁기", "TV"]

CATEGORY_KEYWORDS = {
    "생활용품, 주방용품, 욕실용품": "주방용품 생활용품",
    "문구, 사무용품": "문구 사무용품",
    "인테리어 소품, 수납용품": "인테리어소품 수납용품",
    "장난감, 완구": "장난감 완구",
    "반려동물 용품": "반려동물용품",
}

def scrape_naver_shopping(keyword: str, client_id: str, client_secret: str, max_items: int = 20) -> List[Dict[str, Any]]:
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": keyword,
        "display": max_items,
        "sort": "sim",
    }
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        items = []
        for item in data.get("items", []):
            title = item.get("title", "").replace("<b>", "").replace("</b>", "")
            if any(ex in title for ex in EXCLUDE_KEYWORDS):
                continue
            items.append({
                "title": title,
                "price": item.get("lprice", "N/A"),
                "image": item.get("image", ""),
                "url": item.get("link", "#"),
                "sales": "N/A",
                "reviews": item.get("reviewCount", "N/A"),
                "source": "네이버 쇼핑"
            })
        if not items:
            raise Exception("상품을 찾지 못했습니다.")
        return items
    except requests.exceptions.RequestException as e:
        raise Exception(f"네트워크 오류: {e}")

def scrape_aliexpress_api(keyword: str = "", app_key: str = "", app_secret: str = "", tracking_id: str = "", max_items: int = 20) -> List[Dict[str, Any]]:
    raise Exception("네이버 API 키를 입력해주세요.")