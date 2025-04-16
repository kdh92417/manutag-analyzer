import streamlit as st
import json
from collections import Counter
import pandas as pd

def extract_and_count_manu_tag_keywords(products):
    all_keywords = []
    manu_list = []

    for i, product in enumerate(products, 1):
        manu_tag = product.get("manuTag", "")
        if manu_tag is None:
            manu_tag = ""

        manu_list.append({"index": i, "manuTag": manu_tag})

        if manu_tag.strip() == "":
            all_keywords.append("(empty)")
        else:
            splitted = [tag.strip() for tag in manu_tag.split(',')]
            for tag in splitted:
                all_keywords.append(tag if tag != "" else "(empty)")

    counter = Counter(all_keywords)
    sorted_by_freq = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    return sorted_by_freq, manu_list

# 페이지 설정
st.set_page_config(page_title="manuTag 키워드 분석기", layout="wide")

# 제목
st.title("🔍 manuTag 키워드 분석기")

# JSON 입력창
json_input = st.text_area("📥 JSON 입력", height=600, placeholder="여기에 JSON 문자열을 입력하세요...", key="large_input_area")

# 분석 버튼
if st.button("📊 분석 시작하기"):
    if json_input.strip() == "":
        st.warning("⚠️ JSON 문자열을 입력한 후 버튼을 눌러주세요.")
    else:
        try:
            raw_data = json.loads(json_input)

            if isinstance(raw_data, list):
                products = raw_data
            elif isinstance(raw_data, dict):
                products = raw_data.get("shoppingResult", {}).get("products", [])
                if not isinstance(products, list):
                    st.error("❌ 'products' 키가 리스트 형태여야 합니다.")
                    st.stop()
            else:
                st.error("❌ 올바르지 않은 JSON 구조입니다.")
                st.stop()

            if not products:
                st.warning("⚠️ 'products' 리스트가 비어있습니다.")
            else:
                sorted_keywords, manu_list = extract_and_count_manu_tag_keywords(products)

                st.subheader("📋 전체 manuTag 목록")
                st.dataframe(pd.DataFrame(manu_list), use_container_width=True)

                st.subheader("📊 키워드 별 등장 횟수")
                df = pd.DataFrame(sorted_keywords, columns=["키워드", "빈도수"])
                st.dataframe(df, use_container_width=True)

        except json.JSONDecodeError as e:
            st.error(f"❌ JSON 파싱 오류: {e}")
        except Exception as e:
            st.error(f"⚠️ 처리 중 오류 발생: {e}")
