import os
import re
import streamlit as st
from scraper import scrape_naver_shopping

st.set_page_config(page_title="펀타 소싱에이전트", page_icon="🛍️", layout="wide")

CATEGORIES = {
    "생활용품": {
        "주방용품": ["냄비", "프라이팬", "주방수납", "주방소품", "컵", "텀블러"],
        "욕실용품": ["칫솔", "샴푸용품", "욕실수납", "욕실소품", "비누"],
        "청소용품": ["청소도구", "청소포", "쓰레기통", "빨래용품"],
        "수납정리": ["수납함", "정리함", "바구니", "서랍정리"],
    },
    "문구/사무용품": {
        "필기구": ["볼펜", "샤프", "형광펜", "마커"],
        "노트/다이어리": ["노트", "다이어리", "메모지", "스티커"],
        "사무소품": ["테이프", "가위", "클립", "파일"],
        "데스크소품": ["펜꽂이", "책상정리", "메모보드"],
    },
    "인테리어": {
        "소품": ["캔들", "디퓨저", "액자", "화분"],
        "패브릭": ["쿠션", "방석", "러그", "커튼"],
        "조명": ["무드등", "스탠드", "LED조명"],
        "시계/거울": ["벽시계", "탁상시계", "거울"],
    },
    "장난감/완구": {
        "유아완구": ["블록", "인형", "유아장난감"],
        "퍼즐/보드게임": ["퍼즐", "보드게임", "카드게임"],
        "야외완구": ["비누방울", "물총", "공놀이"],
    },
    "반려동물": {
        "강아지용품": ["강아지간식", "강아지장난감", "강아지옷"],
        "고양이용품": ["고양이장난감", "고양이간식", "캣타워"],
        "공통용품": ["반려동물수납", "펫용품", "동물장난감"],
    },
    "뷰티소품": {
        "메이크업소품": ["화장솔", "파우치", "거울소품"],
        "스킨케어소품": ["면봉", "화장솜", "스킨케어소품"],
        "헤어소품": ["헤어핀", "헤어밴드", "헤어소품"],
    },
    "파티/시즌": {
        "파티용품": ["파티소품", "풍선", "가랜드"],
        "시즌소품": ["크리스마스소품", "할로윈소품", "생일소품"],
    },
    "캠핑/야외": {
        "캠핑소품": ["캠핑식기", "캠핑소품", "피크닉용품"],
        "야외소품": ["돗자리", "아이스팩", "야외테이블"],
    },
}

TRENDING_KEYWORDS = ["생활소품", "주방소품", "인테리어소품", "다이소스타일", "수납용품", "홈데코", "소품샵"]

client_id = os.environ.get("NAVER_CLIENT_ID", "")
client_secret = os.environ.get("NAVER_CLIENT_SECRET", "")

def extract_keywords(items, base_keyword):
    word_count = {}
    stopwords = ["세트", "팩", "개입", "증정", "무료", "배송", "특가", "할인", "신상", "국내", "정품", "추천", "인기", "베스트"]
    for item in items:
        title = re.sub(r"<[^>]+>", "", item.get("title", ""))
        words = re.findall(r"[가-힣]{2,5}", title)
        for word in words:
            if word != base_keyword and word not in stopwords:
                word_count[word] = word_count.get(word, 0) + 1
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [w for w, c in sorted_words][:20]

st.markdown("""<style>
.product-card { border: 1px solid #eee; border-radius: 8px; padding: 15px; margin-bottom: 20px; }
.product-title { font-size: 14px; font-weight: 600; margin-top: 10px; color: #333; }
.product-price { color: #ff3c3c; font-size: 18px; font-weight: bold; margin-top: 5px; }
.product-stats { font-size: 12px; color: #777; margin-top: 3px; }
.btn-link { display: inline-block; text-decoration: none; background-color: #03C75A; color: white; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: bold; margin-top: 10px; width: 100%; text-align: center; }
.keyword-tag { display: inline-block; background-color: #f0f4ff; color: #3358cc; padding: 4px 10px; border-radius: 20px; font-size: 13px; margin: 3px; border: 1px solid #c0ccee; }
</style>""", unsafe_allow_html=True)

st.title("🛍️ 펀타 소싱에이전트")

col_search, col_btn = st.columns([5, 1])
with col_search:
    direct_keyword = st.text_input("검색어", placeholder="직접 검색어 입력 (예: 수납함, 텀블러, 캔들...)", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    direct_btn = st.button("검색 🔍", type="primary")

if direct_btn and direct_keyword:
    if not client_id or not client_secret:
        st.error("환경변수에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요!")
    else:
        st.session_state['keyword'] = direct_keyword
        st.session_state['label'] = "직접 검색 > " + direct_keyword
        st.session_state['search'] = True

st.divider()

with st.sidebar:
    st.header("🔍 검색 모드")
    mode = st.radio("모드 선택", ["카테고리별 검색", "전체 인기상품"])
    st.divider()
    if mode == "카테고리별 검색":
        st.header("🛒 카테고리 선택")
        cat1 = st.selectbox("1차 카테고리", list(CATEGORIES.keys()))
        cat2 = st.selectbox("2차 카테고리", list(CATEGORIES[cat1].keys()))
        cat3 = st.selectbox("3차 카테고리", CATEGORIES[cat1][cat2])
    else:
        st.header("🔥 인기 키워드 선택")
        trending_kw = st.selectbox("키워드", TRENDING_KEYWORDS)
    st.divider()
    search_btn = st.button("상품 검색 시작 🚀", type="primary")
    if search_btn:
        if not client_id or not client_secret:
            st.error("환경변수에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요!")
        else:
            if mode == "카테고리별 검색":
                st.session_state['keyword'] = cat3
                st.session_state['label'] = cat1 + " > " + cat2 + " > " + cat3
            else:
                st.session_state['keyword'] = trending_kw
                st.session_state['label'] = "전체 인기상품 > " + trending_kw
            st.session_state['search'] = True

if st.session_state.get('search'):
    keyword = st.session_state['keyword']
    label = st.session_state['label']
    st.subheader("✅ [" + label + "] 검색 결과")

    items = []
    with st.spinner("검색 중..."):
        try:
            items = scrape_naver_shopping(keyword, client_id, client_secret, 50)
        except Exception as e:
            st.error("오류: " + str(e))

    if items:
        keywords = extract_keywords(items, keyword)
        st.markdown("**🏷️ 연관 키워드 " + str(len(keywords)) + "개**")
        if keywords:
            tags_html = ""
            for kw in keywords:
                tags_html += '<span class="keyword-tag"># ' + kw + '</span>'
            st.markdown(tags_html, unsafe_allow_html=True)
        st.divider()

        cols = st.columns(4)
        for idx, item in enumerate(items):
            with cols[idx % 4]:
                price = str(int(item['price'])) + "원" if str(item['price']).isdigit() else str(item['price'])
                img = item.get('image', '')
                title = item.get('title', '')
                reviews = str(item.get('reviews', 'N/A'))
                url = item.get('url', '#')
                card = (
                    '<div class="product-card">'
                    '<img src="' + img + '" width="100%" style="border-radius:6px; aspect-ratio:1/1; object-fit:cover;">'
                    '<div class="product-title">' + title + '</div>'
                    '<div class="product-price">' + price + '</div>'
                    '<a href="' + url + '" target="_blank" class="btn-link">네이버 쇼핑 열기</a>'
                    '</div>'
                )
                st.markdown(card, unsafe_allow_html=True)
        st.success("총 " + str(len(items)) + "개 상품을 불러왔습니다!")

    st.session_state['search'] = False