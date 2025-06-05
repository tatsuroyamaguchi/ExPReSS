# -----------------------------------------------------------------------------
# Title   : ExPReSS 0.2
# Author  : tatsuroyamaguchi
# License : CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Created : 2025-05-03
# Modified: 2025-05-16 for FoundationOne XML support
# -----------------------------------------------------------------------------

# app/main.py
import os
import streamlit as st
from utils.data_processing import process_foundationone, process_genminetop, process_guardant360, process_hemsight
from utils.file_handling import create_zip_file
from utils.excel_handling import excel_fasttrack
from utils.sidebar_inputs import render_sidebar_inputs


st.set_page_config(
    page_title="ExPReSS",
    page_icon=":dna:",
    layout="wide",
)


###### Sidebar ######
# Render shared sidebar inputs
inputs = render_sidebar_inputs()
date = inputs['date']
normal_sample = inputs['normal_sample']
ep_institution = inputs['ep_institution']
ep_department = inputs['ep_department']
ep_responsible = inputs['ep_responsible']
ep_contact = inputs['ep_contact']
ep_tel = inputs['ep_tel']

###### Main Content ######
st.title("ExPReSS 0.2")
st.write("Expert Panel Report Support System for Comprehensive Cancer Genomic Profiling")
st.markdown("---")

# Analysis type selection
analysis_type = st.radio(
    "解析タイプを選択してください",
    ("FoundationOne", "FoundationOne Liquid", "GenMineTOP", "Guardant360", "HemeSight", "HemeSight (Fast Track)"),
    horizontal=False
)

# File uploader based on analysis type
if analysis_type == "FoundationOne":
    uploaded_file = st.file_uploader("XMLファイルをアップロードしてください", type="xml")
    file_extension = "xml"
elif analysis_type == "FoundationOne Liquid":
    uploaded_file = st.file_uploader("XMLファイルをアップロードしてください", type="xml")
    file_extension = "xml"
elif analysis_type == "GenMineTOP":
    uploaded_file = st.file_uploader("XMLファイルをアップロードしてください", type="xml")
    file_extension = "xml"
elif analysis_type == "Guardant360":
    uploaded_file = st.file_uploader("XLSXファイルをアップロードしてください", type="xlsx")
    file_extension = "xlsx"
elif analysis_type == "HemeSight":
    uploaded_file = st.file_uploader("JSONファイルをアップロードしてください", type="json")
    file_extension = "json"
elif analysis_type == "HemeSight (Fast Track)":
    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")
    file_extension = "pdf"
    

# Get filename without extension
if uploaded_file is not None:
    file_name = uploaded_file.name.split('.')[0]

# Get current directory and template path
current_dir = os.getcwd()

if uploaded_file is not None:
 
    if analysis_type == "FoundationOne":  # FoundationOne
        xml_data = uploaded_file.read().decode('utf-8')
        template_file = os.path.join(current_dir, "app/template/Template_FoundationOne.xlsx")
        if st.button('Run'):
            output_stream = process_foundationone(
                analysis_type, xml_data, template_file, date, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )

            st.download_button(
                label="Download Processed Excel",
                data=output_stream.getvalue(),
                file_name=file_name + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    elif analysis_type == "FoundationOne Liquid":  # FoundationOne Liquid
        xml_data = uploaded_file.read().decode('utf-8')
        template_file = os.path.join(current_dir, "app/template/Template_FoundationOne.xlsx")
        if st.button('Run'):
            output_stream = process_foundationone(
                analysis_type, xml_data, template_file, date, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )

            st.download_button(
                label="Download Processed Excel",
                data=output_stream.getvalue(),
                file_name=file_name + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    elif analysis_type == "GenMineTOP":  # GenMineTOP
        xml_data = uploaded_file.read().decode('utf-8')
        template_file = os.path.join(current_dir, "app/template/Template_GenMineTOP.xlsx")
        if st.button('Run'):
            output_stream = process_genminetop(
                analysis_type, xml_data, template_file, date, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )

            st.download_button(
                label="Download Processed Excel",
                data=output_stream.getvalue(),
                file_name=file_name + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
    elif analysis_type == "Guardant360":  # Guardant360
        xlsx_data = uploaded_file.read()
        template_file = os.path.join(current_dir, "app/template/Template_Guardant360.xlsx")
        if st.button('Run'):
            output_stream = process_guardant360(
                analysis_type, xlsx_data, template_file, date, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )

            st.download_button(
                label="Download Processed Excel",
                data=output_stream.getvalue(),
                file_name=file_name + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    if analysis_type == "HemeSight":
        json_data = uploaded_file.read().decode('utf-8')
        template_file = os.path.join(current_dir, "app/template/Template_HemeSight.xlsx")
        if st.button('Run'):
            output_stream, proteinpaint_path, disco_path = process_hemsight(
                analysis_type, json_data, template_file, date, normal_sample, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )
            
            # Individual download buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="Download Processed Excel",
                    data=output_stream.getvalue(),
                    file_name=file_name + '.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            with col2:
                st.download_button(
                    label="Download ProteinPaint Data",
                    data=open(proteinpaint_path, 'rb').read(),
                    file_name=file_name + 'proteinpaint.tsv',
                    mime='text/tab-separated-values'
                )
            
            with col3:
                st.download_button(
                    label="Download Disco Data",
                    data=open(disco_path, 'rb').read(),
                    file_name=file_name + 'disco.tsv',
                    mime='text/tab-separated-values'
                )
            
            # ZIP file with all outputs
            zip_buffer = create_zip_file(file_name, output_stream, proteinpaint_path, disco_path)
            
            # Bulk download button
            st.markdown("### 一括ダウンロード")
            st.download_button(
                label="全てのファイルをダウンロード (ZIP)",
                data=zip_buffer,
                file_name=file_name + '_all_files.zip',
                mime='application/zip'
            )
    
    elif analysis_type == "HemeSight (Fast Track)":  # HemeSight (Fast Track)
        pdf_data = uploaded_file.read()
        template_file = os.path.join(current_dir, "app/template/Template_FastTrack.xlsx")
        if st.button('Run'):
            output_stream = excel_fasttrack(
                analysis_type, pdf_data, template_file, date, ep_institution, ep_department, ep_responsible, ep_contact, ep_tel
            )

            st.download_button(
                label="Download Processed Excel",
                data=output_stream.getvalue(),
                file_name=file_name + '.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

st.markdown("---")
with st.expander("## Link to Public Databases", expanded=False):
    st.markdown("""
                - cBioPortal: https://www.cbioportal.org/
                - CiVIC: https://civicdb.org/
                - CKB Core: https://ckb.jax.org/
                - ClinGen: https://clinicalgenome.org/
                - ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
                - COSMIC: https://cancer.sanger.ac.uk/cosmic
                - dbNSFP: https://sites.google.com/site/jpopgen/dbNSFP
                - dbSNP: https://www.ncbi.nlm.nih.gov/snp/
                - dbVar: https://www.ncbi.nlm.nih.gov/dbvar/
                - Ensembl: https://www.ensembl.org/index.html
                - Franklin: https://franklin.genoox.com/
                - GeneBe: https://www.genebe.org/
                - gnomAD: https://gnomad.broadinstitute.org/
                - ICGC: https://dcc.icgc.org/
                - jMorp: https://jmorp.megabank.tohoku.ac.jp/
                - OMIM: https://omim.org/
                - OncoKB: https://www.oncokb.org/
                - RefSeq: https://www.ncbi.nlm.nih.gov/refseq/
                - TP53 Database: https://tp53.cancer.gov/
                - UCSC: https://genome.ucsc.edu/
                - UniProt: https://www.uniprot.org/
                - Varsome: https://varsome.com/
                """)

with st.expander("## README", expanded=False):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    st.markdown(readme_content)

# パスワードを入力
password = st.text_input("API", type="password")

# 正しいパスワードを設定（必要に応じてハッシュ化なども可能）
correct_password = "123"

# パスワードが正しい場合にのみ表示
if password == correct_password:
    with st.expander("## API", expanded=False):
        st.markdown("""
        ### API
        - echo "machine api.genebe.io login t.yamaguchi.nf@juntendo.ac.jp password Kyosuke1220" >> ~/.netrc
        - genebe account --username t.yamaguchi.nf@juntendo.ac.jp --api_key YOUR_API_KEY
        """)
elif password:  # パスワードが入力されたが間違っていた場合
    st.error("パスワードが間違っています。")
    

# Table作成
st.markdown("---")
st.markdown("""
            | Panel | HemeSight | FoundationOne | FoundationOne Liquid| GenMineTOP | Guardant360 |
            |-------|-----------|---------------|---------------------|------------|-------------|
            | Sample type | Blood/Normal | Tumor | Liquid | Tumor/Normal| Liquid|
            | Nucleic acid | DNA/RNA  DNA | ctDNA | DNA/RNA | ctDNA|
            | # of SNV/Indel | 319 | 324 | 324 | 737 | 74 |
            | # of CNV | - | 309 (Amp/Del) | - | 737 (Amp) | 18 (Amp) |
            | # of rearrangements | 329   | 36 | 36 | 454 | 6 |
            | MSI | - | + | - | - | + |
            | TMB | - | + | - | + | - |
            | Germline | + | - | - | 40 | - |
            | File type | JSON | XML | XML | XML | XLSX |
            | Referrnce genome | GRCh38 | GRCh37(hg19) | GRCh37(hg19) | GRCh38 | GRCh37(hg19) |
            """)
st.markdown("---")