
import streamlit as st
import json
from collections import Counter
import pandas as pd

def extract_and_count_manu_tag_keywords(data):
    all_keywords = []

    st.subheader("📋 각 product의 manuTag 값")
    for i, product in enumerate(data, 1):
        manu_tag = product.get("manuTag", "")
        if manu_tag is None:
            manu_tag = ""

        st.text(f"{i}) {manu_tag}")

        if manu_tag.strip() == "":
            all_keywords.append("(empty)")
        else:
            splitted = [tag.strip() for tag in manu_tag.split(',')]
            for tag in splitted:
                all_keywords.append(tag if tag != "" else "(empty)")

    counter = Counter(all_keywords)
    sorted_by_freq = sorted(counter.items(), key=lambda x: x[1], reverse=True)

    return sorted_by_freq

st.title("🔍 manuTag 키워드 분석기 (텍스트 입력용)")

with st.form("text_input_form"):
    raw_text = st.text_area("JSON 텍스트를 입력해주세요 (product 리스트 형식)", height=300)
    submitted = st.form_submit_button("📊 분석 시작하기")

if submitted:
    try:
        data = json.loads(raw_text)

        if isinstance(data, dict) and "products" in data:
            data = data["products"]

        if not isinstance(data, list):
            st.error("⚠️ JSON 텍스트는 'products' 키를 포함하거나 product 객체 리스트여야 합니다.")
        else:
            sorted_keywords = extract_and_count_manu_tag_keywords(data)

            st.subheader("📊 키워드 별 등장 횟수")
            df = pd.DataFrame(sorted_keywords, columns=["키워드", "빈도수"])
            st.dataframe(df)

    except Exception as e:
        st.error(f"텍스트를 처리하는 중 오류가 발생했습니다: {e}")
