# data_fetch.py

import re
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
from .parameter import DBPaths, URLs, Constants


def fetch_tommo_data(transcript_id, hgvs_p, alt, dbsnp):
    """Fetch frequency information from ToMMo database"""
    primary_keys = Constants.TOMMO_PRIMARY_KEYS
    fallback_key = Constants.TOMMO_FALLBACK_KEY

    def extract_frequency(text, source):
        pattern = re.compile(rf'\b{alt}=(\d\.\d+)[^()]*\((.*?)\)')
        matches = pattern.findall(text)

        for value, src in matches:
            if src in primary_keys:
                try:
                    freq = round(float(value) * 100, 3)
                    return f"{src}: {freq}%"
                except ValueError:
                    continue

        gnomad_pattern = re.compile(rf'\b{alt}=(\d\.\d+)[^()]*\({fallback_key}\)')
        gnomad_matches = gnomad_pattern.findall(text)
        if gnomad_matches:
            try:
                freq = round(float(gnomad_matches[0]) * 100, 3)
                return f"{fallback_key}: {freq}%"
            except ValueError:
                pass
        return "-"

    for url in [
        URLs.NCBI_SNP.format(query=f"{transcript_id}:{hgvs_p}"),
        URLs.NCBI_SNP.format(query=dbsnp)
    ]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            supp_section = soup.find(class_="supp")
            if supp_section:
                return extract_frequency(supp_section.get_text(strip=True), url)
        except requests.RequestException as e:
            st.warning(f"ToMMoデータ取得エラー: {e}")
    return "-"


def fetch_clinvar_data(transcript_id, hgvs_c, dbsnp):
    """Fetch ClinVar data and pathogenicity using Entrez API"""
    if 'dup' in hgvs_c:
        hgvs_c = hgvs_c.split('dup')[0] + 'dup'

    def fetch_clinvar_id(query):
        response = requests.get(URLs.CLINVAR_ESEARCH, params={
            "db": "clinvar",
            "term": query,
            "retmode": "json"
        })
        if response.status_code != 200:
            raise Exception(f"Error fetching data from ClinVar: {response.status_code}")
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    query = f'"{transcript_id}:{hgvs_c}"[variant_name]'
    clinvar_ids = fetch_clinvar_id(query)
    if dbsnp and not clinvar_ids:
        query = f'"{dbsnp}"[dbsnp_id]'
        clinvar_ids = fetch_clinvar_id(query)
    if not clinvar_ids:
        return "", "", "", "", ""

    for clinvar_id in clinvar_ids:
        response = requests.get(URLs.CLINVAR_ESUMMARY, params={
            "db": "clinvar",
            "id": clinvar_id,
            "retmode": "json"
        })
        if response.status_code != 200:
            raise Exception(f"Error fetching data from ClinVar: {response.status_code}")
        summary = response.json().get("result", {}).get(clinvar_id, {})
        germline_sig = summary.get("germline_classification", {}).get("description", "NA")
        germline_status = summary.get("germline_classification", {}).get("review_status", "NA")
        somatic_sig = summary.get("oncogenicity_classification", {}).get("description", "NA")
        somatic_status = summary.get("oncogenicity_classification", {}).get("review_status", "NA")
        if germline_sig and somatic_sig:
            break
    return germline_sig, germline_status, somatic_sig, somatic_status, clinvar_id


def fetch_tp53_data(position, ref, alt, gene_symbol):
    """Fetch transactivation class from TP53 database"""
    if gene_symbol != 'TP53':
        return 'Not TP53'

    try:
        tp53_df = pd.read_csv(DBPaths.TP53_CSV, sep=',', encoding='utf-8')
        tp53_df['TP53_GRCh38'] = tp53_df['g_description_GRCh38'].str.replace('g.', '', regex=False)
        match = tp53_df[tp53_df['TP53_GRCh38'].str.contains(f"{position}{ref}>{alt}", na=False)]
        return match.iloc[0]['TransactivationClass'] if not match.empty else 'NA'
    except Exception as e:
        st.warning(f"TP53データ取得エラー: {e}")
        return 'NA'


def fetch_role_tier(gene_symbol):
    """Fetch role and tier information from Cancer Gene Census"""
    try:
        cgc_path = DBPaths.get_cgc_tsv()
        if not cgc_path:
            st.warning("CGCファイルが見つかりません。")
            return None, None, None, None, None

        cgc_df = pd.read_csv(cgc_path, sep='\t', encoding='utf-8')
        match = cgc_df[cgc_df['GENE_SYMBOL'] == gene_symbol]
        if not match.empty:
            return (
                match.iloc[0]['ROLE_IN_CANCER'],
                str(match.iloc[0]['TIER']),
                match.iloc[0]['TUMOUR_TYPES_SOMATIC'],
                match.iloc[0]['TUMOUR_TYPES_GERMLINE'],
                match.iloc[0]['CANCER_SYNDROME']
            )
        return None, None, None, None, None
    except Exception as e:
        st.warning(f"Cancer Gene Censusデータ取得エラー: {e}")
        return None, None, None, None, None


def fetch_cosmic_data(gene_symbol, hgvs_c, hgvs_p):
    """Fetch sample information from COSMIC database"""
    try:
        cosmic_path = DBPaths.get_cosmic_tsv_gz()
        if not cosmic_path:
            st.warning("COSMICファイルが見つかりません。")
            return None, None

        cosmic_df = pd.read_csv(cosmic_path, sep='\t', compression='gzip', encoding='utf-8', low_memory=False)
        match = cosmic_df[
            (cosmic_df['GENE_NAME'] == gene_symbol) &
            ((cosmic_df['Mutation CDS'] == hgvs_c) | (cosmic_df['Mutation AA'] == hgvs_p))
        ]
        return (
            match.iloc[0]['COSMIC_SAMPLE_TESTED'] if not match.empty else None,
            match.iloc[0]['COSMIC_SAMPLE_MUTATED'] if not match.empty else None
        )
    except Exception as e:
        st.warning(f"COSMICデータ取得エラー: {e}")
        return None, None
