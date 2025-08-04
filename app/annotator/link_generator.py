import streamlit as st
import pandas as pd

from .parameter import URLs, DBPaths

def generate_links(chromosome, position, ref, alt, transcript_id, gene_symbol, hgvs_c, hgvs_p):
    """Generate Excel HYPERLINK format links"""
    civic_link = generate_civic_link(gene_symbol)

    values = dict(
        chromosome=chromosome,
        position=position,
        ref=ref,
        alt=alt,
        transcript_id=transcript_id,
        gene_symbol=gene_symbol,
        hgvs_c=hgvs_c,
        hgvs_p=hgvs_p
    )

    links = {
        key: f'=HYPERLINK("{url.format(**values)}", "{key}")'
        for key, url in URLs.LINK_TEMPLATES.items()
    }
    links["CiVIC"] = civic_link if civic_link else "N/A"
    return links

def generate_html_links(chromosome, position, ref, alt, transcript_id, gene_symbol, hgvs_c, hgvs_p):
    """Generate HTML links for display in Streamlit or other frontends"""
    civic_html_link = generate_civic_html_link(gene_symbol)

    values = dict(
        chromosome=chromosome,
        position=position,
        ref=ref,
        alt=alt,
        transcript_id=transcript_id,
        gene_symbol=gene_symbol,
        hgvs_c=hgvs_c,
        hgvs_p=hgvs_p
    )

    links = {
        key: f'<a href="{url.format(**values)}" target="_blank">{key}</a>'
        for key, url in URLs.LINK_TEMPLATES.items()
    }
    links["CiVIC"] = civic_html_link if civic_html_link else "N/A"
    return links

def generate_civic_link(gene_symbol):
    try:
        civic_path = DBPaths.get_civic_tsv()
        if not civic_path:
            st.warning("CiVICファイルが見つかりません。")
            return None

        civic_df = pd.read_csv(civic_path, sep='\t', encoding='utf-8')
        match = civic_df[civic_df['name'] == gene_symbol]
        return f'=HYPERLINK("{match.iloc[0]["feature_civic_url"]}", "CiVIC")' if not match.empty else None
    except Exception as e:
        st.warning(f"CiVICリンク生成エラー: {e}")
        return None

def generate_civic_html_link(gene_symbol):
    """Generate HTML link to CiVIC database for a gene"""
    try:
        civic_path = DBPaths.get_civic_tsv()
        if not civic_path:
            st.warning("CiVICファイルが見つかりません。")
            return "N/A"

        civic_df = pd.read_csv(civic_path, sep='\t', encoding='utf-8')
        match = civic_df[civic_df['name'] == gene_symbol]
        if not match.empty:
            return f'<a href="{match.iloc[0]["feature_civic_url"]}" target="_blank">CiVIC</a>'
        return "N/A"
    except Exception as e:
        st.warning(f"CiVICリンク生成エラー: {e}")
        return "N/A"