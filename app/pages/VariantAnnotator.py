import streamlit as st
import pandas as pd
from annotator.sidebar import setup_sidebar
from annotator.variant_processor import process_variant
from annotator.link_generator import generate_html_links

# ページ設定
st.set_page_config(
    page_title="VariantAnnotator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def annotate_single_variant(grc, variant):
    """単一バリアントの注釈処理と表示"""
    result = process_variant(grc, variant)
    if result:
        df = pd.DataFrame([result])

        html_data = result.copy()
        html_links = generate_html_links(
            result['Chromosome'], result['hg38 Position'], result['Reference Allele'],
            result['Alternate Allele'], result['Transcript ID'], result['Gene Symbol'],
            result['HGVS cDNA'], result['HGVS Protein']
        )
        for key in html_links:
            if key in html_data:
                html_data[key] = html_links[key]

        html_df = pd.DataFrame([html_data])
        st.success("解析完了。以下に結果を表示します。")
        st.markdown(html_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", csv, "annotation_results.csv", "text/csv")


def annotate_csv_variants(grc, uploaded_file):
    """CSVファイルからの複数バリアントの注釈処理と表示"""
    try:
        input_df = pd.read_csv(uploaded_file)
        if 'Variant' not in input_df.columns:
            st.error("CSVに 'Variant' 列が含まれていません。")
            return

        results = []
        html_results = []

        st.info("注釈を処理中...")
        for idx, row in input_df.iterrows():
            st.write(f"Processing {idx + 1}/{len(input_df)}: {row['Variant']}")
            result = process_variant(grc, row['Variant'])
            if result:
                result['Variant'] = row['Variant']
                results.append(result)

                html_data = result.copy()
                html_links = generate_html_links(
                    result['Chromosome'], result['hg38 Position'], result['Reference Allele'],
                    result['Alternate Allele'], result['Transcript ID'], result['Gene Symbol'],
                    result['HGVS cDNA'], result['HGVS Protein']
                )
                for key in html_links:
                    if key in html_data:
                        html_data[key] = html_links[key]
                html_results.append(html_data)

        if results:
            result_df = pd.DataFrame(results)
            html_df = pd.DataFrame(html_results)

            st.success("解析完了。以下に結果を表示します。")
            st.markdown(html_df.to_html(escape=False, index=False), unsafe_allow_html=True)

            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results as CSV", csv, "annotation_results.csv", "text/csv")
        else:
            st.warning("解析可能なバリアントが見つかりませんでした。")

    except Exception as e:
        st.error(f"ファイル処理エラー: {e}")


def main():
    """メインアプリケーション"""
    st.title("🧬 VariantAnnotator")
 
    grc, variant = setup_sidebar()

    if st.sidebar.button("Run Annotation"):
        annotate_single_variant(grc, variant)

    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader("Upload CSV with 'Variant' column", type=["csv"])

    if st.sidebar.button("Run") and uploaded_file:
        annotate_csv_variants(grc, uploaded_file)
    
    with st.expander("## README", expanded=False):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        st.markdown(readme_content)
       

if __name__ == "__main__":
    main()
