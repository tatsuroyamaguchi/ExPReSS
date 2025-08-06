import re
import math
from io import BytesIO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from matplotlib.patches import Patch
import streamlit as st

from annotator.parser import parse_foundationone_xml
from annotator.parameter import SummaryViewerF1


st.set_page_config(
    page_title="SummaryViewer for F1",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🧬 SummaryViewer for FoundationOne")

uploaded_files = st.sidebar.file_uploader("Upload XML files", type="xml", accept_multiple_files=True)
# --- 重複するファイルを削除 ---
if uploaded_files:
    # ファイル名を基準に重複を除去
    seen_filenames = set()
    unique_files = []
    for file in uploaded_files:
        if file.name not in seen_filenames:
            unique_files.append(file)
            seen_filenames.add(file.name)
    st.success(f"{len(unique_files)} unique files have been uploaded.")
    uploaded_files = unique_files

if uploaded_files:
    all_sv, all_cna, all_re, all_msi_tmb, all_nh, all_qc = [], [], [], [], [], []

    for file in uploaded_files:
        content = file.read().decode("utf-8")
        df_sv, df_cna, df_re, df_msi_tmb, df_nh, df_qc = parse_foundationone_xml(content)
        all_sv.append(df_sv)
        all_cna.append(df_cna)
        all_re.append(df_re)
        all_msi_tmb.append(df_msi_tmb)
        all_nh.append(df_nh)
        all_qc.append(df_qc)

    df_sv_all = pd.concat(all_sv, ignore_index=True)
    df_cna_all = pd.concat(all_cna, ignore_index=True)
    df_re_all = pd.concat(all_re, ignore_index=True)
    df_msi_tmb_all = pd.concat(all_msi_tmb, ignore_index=True)
    df_nh_all = pd.concat(all_nh, ignore_index=True)
    df_qc_all = pd.concat(all_qc, ignore_index=True)

    # --- 表示 ---
    tabs = st.tabs(["Short Variants", "Copy Number", "Rearrangements", "MSI/TMB", "Non-Human", "Quality Control"])
    with tabs[0]: st.dataframe(df_sv_all)
    with tabs[1]: st.dataframe(df_cna_all)
    with tabs[2]: st.dataframe(df_re_all)
    with tabs[3]: st.dataframe(df_msi_tmb_all)
    with tabs[4]: st.dataframe(df_nh_all)
    with tabs[5]: st.dataframe(df_qc_all)

    # --- Excel出力 ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_sv_all.to_excel(writer, index=False, sheet_name='ShortVariants')
        df_cna_all.to_excel(writer, index=False, sheet_name='CopyNumber')
        df_re_all.to_excel(writer, index=False, sheet_name='Rearrangements')
        df_msi_tmb_all.to_excel(writer, index=False, sheet_name='MSI_TMB')
        df_nh_all.to_excel(writer, index=False, sheet_name='NonHuman')
        df_qc_all.to_excel(writer, index=False, sheet_name='QualityControl')
    output.seek(0)

    st.download_button(
        label="⬇️ Save in Excel format (all sheets)",
        data=output,
        file_name="foundationone_all.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # --- グラフ表示 ---
    st.subheader("Vidualization")
    
    df = df_qc_all.copy()    
    df['Disease'] = df['Disease'].replace('', 'UNKNOWN')
    grouped_df = df.groupby(['Disease', 'Gender']).size().reset_index(name='Count')
    chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Disease:N', sort='-y', title='Disease'),
        y=alt.Y('Count:Q', title='Count'),
        color=alt.Color('Gender:N', scale=alt.Scale(range=['#e377c2', '#1f77b4'])),
        tooltip=['Disease', 'Gender', 'Count']
    ).properties(width=600, height=400, title='Gender by Disease').configure_axisX(labelAngle=-90)
    st.altair_chart(chart, use_container_width=True)
    
    df = df_msi_tmb_all.copy()
    grouped_df = df.groupby(['Disease', 'MSI_Status']).size().reset_index(name='Count')
    chart = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Disease:N', sort='-y', title='Disease'),
        y=alt.Y('Count:Q', title='Count'),
        color=alt.Color('MSI_Status:N', scale=alt.Scale(range=['#ff7f0e', '#999999', '#1f77b4', '#cccccc'])),
        tooltip=['Disease', 'MSI_Status', 'Count']
    ).properties(width=600, height=400, title='MSI status by Disease').configure_axisX(labelAngle=-90)
    st.altair_chart(chart, use_container_width=True)
    
    df = df_msi_tmb_all.copy()
    df['Disease'] = df['Disease'].fillna('UNKNOWN').replace('', 'UNKNOWN')
    df['TMB_Score'] = pd.to_numeric(df['TMB_Score'], errors='coerce')
    df = df.dropna(subset=['TMB_Score'])
    sort_order = df.groupby('Disease')['TMB_Score'].median().sort_values(ascending=True).index.tolist()
    chart = alt.Chart(df).mark_boxplot(color='#1f77b4').encode(
        x=alt.X('Disease:N', sort=sort_order, title='Disease'),
        y=alt.Y('TMB_Score:Q', title='TMB Score'),
        tooltip=['Disease', 'TMB_Score']
    ).properties(
        width=600,
        height=400,
        title='TMB Score by Disease'
    ).configure_axisX(labelAngle=-90)
    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
    # --- 検出遺伝子の頻度をbar chartとして表示 ---
    st.subheader("Histogram of Genes")
    disease_filter = st.sidebar.selectbox("Select Disease", options=['All'] + sorted(df_sv_all['Disease'].unique().tolist()))
    if disease_filter != 'All':
        df_sv_all = df_sv_all[df_sv_all['Disease'] == disease_filter]
        df_cna_all = df_cna_all[df_cna_all['Disease'] == disease_filter]
        df_re_all = df_re_all[df_re_all['Disease'] == disease_filter]
    gender_filter = st.sidebar.selectbox("Select Gender", options=['All'] + df_sv_all['Gender'].unique().tolist())
    if gender_filter != 'All':
        df_sv_all = df_sv_all[df_sv_all['Gender'] == gender_filter]
        df_cna_all = df_cna_all[df_cna_all['Gender'] == gender_filter]
        df_re_all = df_re_all[df_re_all['Gender'] == gender_filter]
                
    st.write("#### Short Variants (known or likely)")
    num_genes = st.slider("Number of genes (SNV)", min_value=1, max_value=100, value=30, step=1)
    df_sv_all = df_sv_all[df_sv_all['Status'] != 'unknown']
    gene_counts = df_sv_all['Gene'].value_counts().reset_index()
    gene_counts.columns = ['Gene', 'Count']
    top_genes = gene_counts.head(num_genes)
    gene_chart = alt.Chart(top_genes).mark_bar().encode(
        x=alt.X('Gene:N', sort='-y', title='Gene'),
        y=alt.Y('Count:Q', title='Count'),
        tooltip=['Gene', 'Count']
    ).properties(width=600, height=400)
    st.altair_chart(gene_chart, use_container_width=True)
    
    st.write("#### Copy Number Alterations (known or likely)")
    num_genes_cna = st.slider("Number of genes（CNA）", min_value=1, max_value=100, value=20, step=1)
    df_cna_all = df_cna_all[df_cna_all['Status'] != 'unknown']
    gene_counts_cna = df_cna_all['Gene'].value_counts().reset_index()
    gene_counts_cna.columns = ['Gene', 'Count']
    top_genes_cna = gene_counts_cna.head(num_genes_cna)
    gene_chart_cna = alt.Chart(top_genes_cna).mark_bar().encode(
        x=alt.X('Gene:N', sort='-y', title='Gene'),
        y=alt.Y('Count:Q', title='Count'),
        tooltip=['Gene', 'Count']
    ).properties(width=600, height=400)
    st.altair_chart(gene_chart_cna, use_container_width=True)
    
    st.write("#### Rearrangements (known or likely)")
    num_genes_re = st.slider("Number of genes（Rearrangements）", min_value=1, max_value=100, value=20, step=1)
    df_re_all = df_re_all[df_re_all['Status'] != 'unknown']
    gene_counts_re = df_re_all['TargetedGene'].value_counts().reset_index()
    gene_counts_re.columns = ['TargetedGene', 'Count']
    top_genes_re = gene_counts_re.head(num_genes_re)
    gene_chart_re = alt.Chart(top_genes_re).mark_bar().encode(
        x=alt.X('TargetedGene:N', sort='-y', title='Gene'),
        y=alt.Y('Count:Q', title='Count'),
        tooltip=['TargetedGene', 'Count']
    ).properties(width=600, height=400)
    st.altair_chart(gene_chart_re, use_container_width=True)
    
    st.write("#### Short Variants (known or likely)")
    df_sv_all['Gene_Protein'] = df_sv_all['Gene'] + ' (' + df_sv_all['Protein_Effect'] + ')'
    df_sv_all = df_sv_all[df_sv_all['Status'] != 'unknown']
    variant_counts = df_sv_all['Gene_Protein'].value_counts().reset_index()
    variant_counts.columns = ['Gene_Protein', 'Count']
    top_variants = variant_counts.head(20)
    variant_chart = alt.Chart(top_variants).mark_bar().encode(
        y=alt.Y('Gene_Protein:N', sort='-x', title='Variant'),
        x=alt.X('Count:Q', title='Count'),
        tooltip=['Gene_Protein', 'Count']
    ).properties(width=600, height=600, title='Top 20').configure_axisY(labelAngle=0)
    st.altair_chart(variant_chart, use_container_width=True)
    
    # --- OncoPrint ---
    st.sidebar.markdown("---")
    st.subheader("OncoPrint")
    
    # Simplify ShortVariants
    def simplify_variant_effect(effect):
        effect = effect.lower() if isinstance(effect, str) else ""
        if effect == "missense":
            return "MISSENSE"
        elif effect == "frameshift":
            return "FRAMESHIFT"
        elif effect == "nonsense":
            return "NONSENSE"
        elif effect == "splice":
            return "SPLICE"
        elif effect == "nonframeshift":
            return "NONFRAMESHIFT"
        else:
            return "OTHER"

    df_sv_filtered = df_sv_all[df_sv_all['Status'] != 'unknown'].copy()
    df_sv_filtered["Alteration"] = df_sv_filtered["Functional_Effect"].apply(simplify_variant_effect)
    df_sv_filtered = df_sv_filtered[df_sv_filtered["Alteration"].isin(SummaryViewerF1.VALID_ALTERATIONS)]
    short_variants_df = df_sv_filtered[["ReferenceID", "Gene", "Alteration"]]

    # Simplify CopyNumber
    def simplify_copy_number(type_val):
        type_val = type_val.lower() if isinstance(type_val, str) else ""
        if type_val == "amplification":
            return "AMPLIFICATION"
        elif type_val == "loss":
            return "LOSS"
        else:
            return "OTHER"

    df_cna_filtered = df_cna_all[df_cna_all['Status'] != 'unknown'].copy()
    df_cna_filtered["Alteration"] = df_cna_filtered["Type"].apply(simplify_copy_number)
    df_cna_filtered = df_cna_filtered[df_cna_filtered["Alteration"].isin(SummaryViewerF1.VALID_ALTERATIONS)]
    copy_number_df = df_cna_filtered[["ReferenceID", "Gene", "Alteration"]]

    # Simplify Rearrangements
    def simplify_rearrangement(type_val):
        type_val = type_val.lower() if isinstance(type_val, str) else ""
        if "fusion" in type_val:
            return "FUSION"
        elif "truncation" in type_val:
            return "TRUNCATION"
        elif "deletion" in type_val:
            return "DELETION"
        elif "duplication" in type_val:
            return "DUPLICATION"
        else:
            return "REARRANGEMENT"

    df_re_filtered = df_re_all[df_re_all['Status'] != 'unknown'].copy()
    df_re_filtered["Alteration"] = df_re_filtered["Type"].apply(simplify_rearrangement)
    df_re_filtered = df_re_filtered[df_re_filtered["Alteration"].isin(SummaryViewerF1.VALID_ALTERATIONS)]
    rearrangements_df = df_re_filtered[["ReferenceID", "TargetedGene", "Alteration"]].rename(columns={"TargetedGene": "Gene"})

    # Combine all alterations
    df_variant = pd.concat([short_variants_df, copy_number_df, rearrangements_df], ignore_index=True)

    # Limit to top N genes based on frequency
    num_genes_oncoprint = st.slider("Number of genes", min_value=5, max_value=50, value=20, step=1)
    gene_counts = df_variant['Gene'].value_counts().head(num_genes_oncoprint).index
    df_variant = df_variant[df_variant['Gene'].isin(gene_counts)]

    # Create pivot table for OncoPrint (遺伝子を行、サンプルを列に)
    df_variant["Alteration"] = df_variant["Alteration"].fillna("UNKNOWN")

    # df_msi_tmb_allの'MSI_Status'と'TMB_Score'と'Gender'をReferenceIDに基づいてonco_matrixに'MSI_Status'と'TMB_Score'行を作成してappend
    if 'MSI_Status' in df_msi_tmb_all.columns and 'TMB_Score' in df_msi_tmb_all.columns:
        df_gender = df_msi_tmb_all.set_index('ReferenceID')['Gender']
        df_disease = df_msi_tmb_all.set_index('ReferenceID')['Disease']
        df_msi = df_msi_tmb_all.set_index('ReferenceID')['MSI_Status']
        df_tmb = df_msi_tmb_all.set_index('ReferenceID')['TMB_Score']
        # sample_type：ReferenceIDに'L'が含まれる場合は'FoundationOne Liquid'、それ以外は'FoundationOne'とする
        df_msi_tmb_all['Sample_Type'] = df_msi_tmb_all['ReferenceID'].apply(lambda x: 'FoundationOne Liquid' if 'L' in x else 'FoundationOne')
        df_sample_type = df_msi_tmb_all.set_index('ReferenceID')['Sample_Type']

    ######################################
    # Input: df_variant, df_gender, df_disease, df_msi, df_tmb, df_sample_type
    
    # Colomn Names: 
    # df_variant: DataFrame with columns ['ReferenceID', 'Gene', 'Alteration']
    # df_gender: DataFrame with columns ['ReferenceID', 'Gender']
    # df_disease: DataFrame with columns ['ReferenceID', 'Disease']
    # df_msi: DataFrame with columns ['ReferenceID', 'MSI_Status']
    # df_tmb: DataFrame with columns ['ReferenceID', 'TMB_Score']
    # df_sample_type: DataFrame with columns ['ReferenceID', 'Sample_Type']
    
    st.markdown("---")
    def onco_print(df_variant, df_gender, df_disease, df_msi, df_tmb, df_sample_type, sample_name='ReferenceID'):
    
        gender_score = df_gender.to_dict()
        disease_name = df_disease.to_dict()
        msi_status = df_msi.to_dict()
        tmb_score = df_tmb.to_dict()
        sample_type = df_sample_type.to_dict()
        
        onco_matrix = df_variant.pivot_table(
            index='Gene',  # 遺伝子を行に
            columns=sample_name,  # サンプルを列に
            values='Alteration',
            aggfunc=lambda x: ','.join(x)
        ).fillna('')
                
        # onco_matrixについて、文字列が含まれるセルの数を調べて降順に並べ替え
        onco_matrix['Count'] = onco_matrix.apply(lambda x: x.str.strip().astype(bool).sum(), axis=1)
        onco_matrix = onco_matrix.sort_values(by='Count', ascending=True)
        sorted_genes = onco_matrix.index.tolist()
        onco_matrix = onco_matrix.sort_values(by='Count', ascending=False)
        onco_matrix = onco_matrix.apply(lambda col: col.map(lambda x: 'OTHER' if ',' in str(x) else x))

        def reorder_columns(df, sorted_genes):
            # 各遺伝子の文字列があるサンプルの列を左に寄せる
            for gene in sorted_genes:
                if gene in df.index:
                    # 文字列があるサンプルの列を取得
                    cols_with_data = df.loc[gene][df.loc[gene].str.strip() != ''].index.tolist()
                    # 文字列がないサンプルの列を取得
                    cols_without_data = df.loc[gene][df.loc[gene].str.strip() == ''].index.tolist()
                    # 新しい順序で列を再配置
                    new_order = cols_with_data + cols_without_data
                    df = df.reindex(columns=new_order, fill_value='')
            return df   
        onco_matrix = reorder_columns(onco_matrix, sorted_genes)
        
        # 遺伝子を先頭にするオプション
        gene_selected = st.selectbox("Select the gene to place on the first row", options=['All'] + sorted(set(df_sv_all['Gene'].unique()) | set(df_cna_all['Gene'].unique()) | set(df_re_all['TargetedGene'].unique())), index=0)
        onco_matrix = reorder_columns(onco_matrix, [gene_selected]) if gene_selected != 'All' else onco_matrix
        # gene_selectedを先頭行に異動
        if gene_selected != 'All' and gene_selected in onco_matrix.index:
            onco_matrix = pd.concat([onco_matrix.loc[[gene_selected]], onco_matrix.drop(gene_selected)], axis=0)

        # Add MSI_Status and TMB_Score rows
        onco_matrix.loc['Sample_Type'] = onco_matrix.columns.map(sample_type).fillna('').astype(str)
        onco_matrix.loc['Gender'] = onco_matrix.columns.map(gender_score).fillna('').astype(str)
        onco_matrix.loc['Disease'] = onco_matrix.columns.map(disease_name).fillna('').astype(str)
        onco_matrix.loc['MSI_Status'] = onco_matrix.columns.map(msi_status).fillna('').astype(str)
        onco_matrix.loc['TMB_Score'] = onco_matrix.columns.map(tmb_score).fillna('').astype(str)


        # OncoPrint描画前に、ソート用の'Count'列を削除
        if 'Count' in onco_matrix.columns:
            onco_matrix = onco_matrix.drop('Count', axis=1)
            
        # OncoPrint描画 with Seaborn
        if not onco_matrix.empty:
            try:
                # Diseaseの情報を動的に取得
                unique_diseases = []
                if 'Disease' in onco_matrix.index:
                    unique_diseases = sorted([d for d in onco_matrix.loc['Disease'].unique() if d and d.lower() != 'unknown'])

                # GenderとMSI_Statusの情報を動的に取得
                unique_genders = []
                if 'Gender' in onco_matrix.index:
                    unique_genders = sorted([g for g in onco_matrix.loc['Gender'].unique() if g and g.lower() != 'unknown'])

                unique_msi_statuses = []
                if 'MSI_Status' in onco_matrix.index:
                    unique_msi_statuses = sorted([m for m in onco_matrix.loc['MSI_Status'].unique() if m and m.lower() != 'unknown'])
                
                unique_sample_types = []
                if 'Sample_Type' in onco_matrix.index:
                    unique_sample_types = sorted([s for s in onco_matrix.loc['Sample_Type'].unique() if s and s.lower() != 'unknown'])

                # VALID_ALTERATIONSに'UNKNOWN'を追加
                genetic_alterations = [
                    alt for alt in SummaryViewerF1.VALID_ALTERATIONS 
                ]
                extended_valid_alterations = genetic_alterations + ['UNKNOWN'] + unique_diseases + unique_genders + unique_msi_statuses + unique_sample_types

                # Disease用のカラー
                disease_colors = sns.color_palette("tab20", n_colors=len(unique_diseases))
                for disease, color in zip(unique_diseases, disease_colors):
                    SummaryViewerF1.COLOR_MAP[disease] = color


                # TMB_Scoreを一時的に取り出して除外
                tmb_row = onco_matrix.loc['TMB_Score'] if 'TMB_Score' in onco_matrix.index else None
                heatmap_matrix = onco_matrix.drop(index='TMB_Score', errors='ignore')

                # 変異を数値に変換（拡張したマッピングを使用）
                alteration_map = {alt: i + 1 for i, alt in enumerate(extended_valid_alterations)}
                alteration_map[''] = 0
                # 未定義の値を'UNKNOWN'に変換
                heatmap_matrix = heatmap_matrix.apply(lambda x: x.map(lambda v: v if v in alteration_map else 'UNKNOWN'))
                heatmap_data = heatmap_matrix.apply(lambda x: x.map(alteration_map)).fillna(0).astype(int)

                # 各サンプルのバリアント数（種類ごと）を計算（Disease, Gender, MSI_Status, TMB_Scoreを除外）
                variant_counts_by_type = {}
                excluded_rows = ['Disease', 'Gender', 'MSI_Status', 'TMB_Score', 'Sample_Type']
                filtered_heatmap_matrix = heatmap_matrix.drop(index=[row for row in excluded_rows if row in heatmap_matrix.index], errors='ignore')
                for sample in heatmap_data.columns:
                    sample_data = filtered_heatmap_matrix[sample]
                    alteration_counts = sample_data[sample_data != ''].value_counts()
                    variant_counts_by_type[sample] = alteration_counts

                # カラーマップ（拡張したカラーマップを使用）
                colors = ['#eeeeee'] + [SummaryViewerF1.COLOR_MAP.get(alt, '#d3d3d3') for alt in extended_valid_alterations]
                cmap = sns.color_palette(colors, as_cmap=False)

                # 描画設定：上部にヒストグラム用のスペースを追加
                fig = plt.figure(figsize=(18, 12))
                gs = fig.add_gridspec(2, 2, height_ratios=[1, 5], width_ratios=[5, 1], wspace=0.02, hspace=0.05)

                # 上部の縦棒ヒストグラム（サンプルごとのバリアント数、種類ごとに色分け）
                ax0 = fig.add_subplot(gs[0, 0])
                bar_width = 1.0
                x_positions = range(len(heatmap_data.columns))
                bottom = np.zeros(len(heatmap_data.columns))
                
                # 各変異タイプについて積み上げ棒グラフを描画（Disease, Gender, MSI_Statusを除外）
                alteration_types = genetic_alterations  # 遺伝子変異のみ
                for alt_type in alteration_types:
                    counts = [variant_counts_by_type.get(sample, {}).get(alt_type, 0) for sample in heatmap_data.columns]
                    ax0.bar(x_positions, counts, bar_width, bottom=bottom, 
                            color=SummaryViewerF1.COLOR_MAP.get(alt_type, '#d3d3d3'), 
                            label=alt_type if sum(counts) > 0 else None, 
                            align='edge')
                    bottom += np.array(counts)

                ax0.set_xlim(0, len(heatmap_data.columns))
                ax0.set_ylabel('Variant Count', fontsize=10)
                ax0.set_xticks([])  # X軸のメモリを非表示
                ax0.grid(axis='y', alpha=0.3)
                
                # メインのOncoPrint
                ax1 = fig.add_subplot(gs[1, 0])
                sns.heatmap(
                    heatmap_data,
                    cmap=cmap,
                    cbar=False,
                    linewidths=0.5,
                    linecolor='#ffffff',
                    ax=ax1
                )

                # TMB_Scoreの棒グラフを最下行に描画
                new_yticks = list(heatmap_data.index)

                if tmb_row is not None:
                    tmb_values = pd.to_numeric(tmb_row, errors='coerce')
                    y_offset = len(heatmap_data)
                    
                    # TMB_Scoreの最大値を取得（NaNを除外）
                    max_tmb = tmb_values.max() if not tmb_values.empty else 30  # デフォルト値として30を使用
                    
                    for x_idx, sample in enumerate(heatmap_data.columns):
                        score = tmb_values.get(sample, None)
                        if pd.notna(score):
                            # TMB_Scoreを最大値でスケーリング
                            bar_height = min(score / max_tmb, 1.0) if max_tmb > 0 else 0
                            ax1.add_patch(plt.Rectangle(
                                (x_idx, y_offset + 1 - bar_height),
                                1.0,
                                bar_height,
                                color='#d62728' if score >= 10 else '#1f77b4',
                                alpha=0.8
                            ))

                    if 'TMB_Score' not in new_yticks:
                        new_yticks.append('TMB_Score')

                # 必要に応じてax1.set_yticks()でy軸ラベルを設定
                ax1.set_yticks(range(len(new_yticks)))
                ax1.set_yticklabels(new_yticks)
                # Y軸の設定
                ax1.set_yticks([i + 0.5 for i in range(len(new_yticks))])
                ax1.set_yticklabels(new_yticks, rotation=0, fontsize=10, fontstyle='italic')
                ax1.set_ylim(len(new_yticks), 0)
                ax1.set_xlabel("", fontsize=12)
                ax1.set_ylabel("Gene", fontsize=12)
                ax1.set_xticklabels([])
                ax1.set_xticks([])

                # 右側の横棒ヒストグラム
                ax2 = fig.add_subplot(gs[1, 1])
                gene_alteration_counts = {}
                for gene in heatmap_matrix.index:
                    if gene not in ['TMB_Score']:
                        gene_data = heatmap_matrix.loc[gene]
                        alteration_counts = gene_data.value_counts()
                        alteration_counts = alteration_counts[alteration_counts.index != '']
                        gene_alteration_counts[gene] = alteration_counts

                bar_height = 0.8
                for i, gene in enumerate(new_yticks):
                    if gene in gene_alteration_counts:
                        alteration_counts = gene_alteration_counts[gene]
                        x_offset = 0
                        for alteration, count in alteration_counts.items():
                            color = SummaryViewerF1.COLOR_MAP.get(alteration, '#d3d3d3')
                            ax2.barh(len(new_yticks) - 1 - i, count,
                                    left=x_offset, height=bar_height,
                                    color=color, alpha=0.8,
                                    edgecolor='white', linewidth=0.5)
                            x_offset += count

                ax2.set_ylim(-0.5, len(new_yticks) - 0.5)
                ax2.set_title('Count', fontsize=12)
                ax2.set_yticks([])
                ax2.grid(axis='x', alpha=0.3)
                ax2.xaxis.set_ticks_position('top')  # Move x-axis ticks to the top

                # 凡例の作成（Alteration用）
                alteration_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP[alt], label=alt)
                    for alt in genetic_alterations
                ]

                num_alterations = len(alteration_legend_elements)
                ncol_alteration = math.ceil(num_alterations / 2)    # 2列に分ける

                # 凡例の作成（Sample_Type用）
                sample_type_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP[stype], label=stype)
                    for stype in unique_sample_types
                ]
                num_sample_types = len(sample_type_legend_elements)
                ncol_sample_type = math.ceil(num_sample_types)

                # 凡例の作成（Disease用）
                disease_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP[disease], label=disease)
                    for disease in unique_diseases
                ]
                num_diseases = len(disease_legend_elements)
                ncol_disease = math.ceil(num_diseases / 3)  # 3列に分ける

                # 凡例の作成（Gender用）
                gender_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP[gender], label=gender)
                    for gender in unique_genders
                ]
                num_genders = len(gender_legend_elements)
                ncol_gender = math.ceil(num_genders)

                # 凡例の作成（MSI_Status用）
                msi_status_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP[msi], label=msi)
                    for msi in unique_msi_statuses
                ]
                num_msi_statuses = len(msi_status_legend_elements)
                ncol_msi_status = math.ceil(num_msi_statuses)

                # 凡例の作成（TMB_Score用）
                tmb_score_legend_elements = [
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP['TMB Score < 10'], label='TMB Score < 10'),
                    Patch(facecolor=SummaryViewerF1.COLOR_MAP['TMB Score >= 10'], label='TMB Score >= 10')
                ]
                num_tmb_scores = len(tmb_score_legend_elements)
                ncol_tmb_score = math.ceil(num_tmb_scores)

                # 凡例の描画
                # Alteration凡例
                if alteration_legend_elements:
                    fig.legend(
                        handles=alteration_legend_elements,
                        bbox_to_anchor=(0.12, 0.20),
                        loc='lower left',
                        ncol=ncol_alteration,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )
                # Sample_Type凡例
                if sample_type_legend_elements:
                    fig.legend(
                        handles=sample_type_legend_elements,
                        bbox_to_anchor=(0.12, 0.18),  # 適切な位置に調整
                        loc='lower left',
                        ncol=ncol_sample_type,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )

                # Gender凡例
                if gender_legend_elements:
                    fig.legend(
                        handles=gender_legend_elements,
                        bbox_to_anchor=(0.12, 0.16),
                        loc='lower left',
                        ncol=ncol_gender,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )

                # Disease凡例
                if disease_legend_elements:
                    fig.legend(
                        handles=disease_legend_elements,
                        bbox_to_anchor=(0.12, 0.10),
                        loc='lower left',
                        ncol=ncol_disease,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )

                # MSI_Status凡例
                if msi_status_legend_elements:
                    fig.legend(
                        handles=msi_status_legend_elements,
                        bbox_to_anchor=(0.12, 0.08),
                        loc='lower left',
                        ncol=ncol_msi_status,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )

                # TMB_Score凡例
                if tmb_score_legend_elements:
                    fig.legend(
                        handles=tmb_score_legend_elements,
                        bbox_to_anchor=(0.12, 0.06),  # Adjust position to avoid overlap
                        loc='lower left',
                        ncol=ncol_tmb_score,
                        fontsize=10,
                        frameon=True,
                        framealpha=0.0
                    )

                plt.subplots_adjust(bottom=0.25)  # 凡例のスペースを確保
                st.pyplot(fig)

            except Exception as e:
                st.error(f"OncoPrintの描画中にエラーが発生しました: {str(e)}")
                st.info("以下のデータフレームを確認して、問題を特定してください。")
                st.subheader("OncoPrintデータ（デバッグ用）")
                st.dataframe(onco_matrix)
        else:
            st.warning("現在のフィルタではOncoPrint用のデータがありません。")
    
    onco_print(df_variant, df_gender, df_disease, df_msi, df_tmb, df_sample_type)
    

    st.markdown("---")
    st.subheader("Lollipop Plot of Variants")

    # Sidebar for selecting gene for Lollipop plot
    gene_options = ['None'] + sorted(set(df_sv_all['Gene'].unique()))
    selected_gene = st.selectbox("Select Gene for Lollipop Plot", options=gene_options, index=0)

    if selected_gene != 'None':
        # Filter Short Variants for the selected gene and apply existing filters
        df_lollipop = df_sv_all[df_sv_all['Gene'] == selected_gene].copy()
        
        # Parse mutation positions from Protein_Effect
        def parse_mutation_position(protein_effect):
            if pd.isna(protein_effect) or not isinstance(protein_effect, str):
                return None

            import re

            # Case 1: splice site, e.g., 'splice site 3954-1G>A'
            if protein_effect.startswith('splice site'):
                match = re.search(r'splice site\s+(\d+)', protein_effect)
                if match:
                    try:
                        genomic_pos = int(match.group(1))
                        return genomic_pos // 3
                    except ValueError:
                        return None
                return None

            # Case 2: promoter region, e.g., 'promoter -146C>T'
            if protein_effect.startswith('promoter'):
                match = re.search(r'promoter\s+(-?\d+)', protein_effect)
                if match:
                    try:
                        promoter_pos = int(match.group(1))
                        return promoter_pos // 3
                    except ValueError:
                        return None
                return None

            # Case 3: protein-level mutation, e.g., 'A552V', 'Q442*', etc.
            match = re.search(r'(\d+)(?:_\w*\d*(?:ins|del))?', protein_effect)
            return int(match.group(1)) if match else None

        df_lollipop['Position'] = df_lollipop['Protein_Effect'].apply(parse_mutation_position)
        df_lollipop = df_lollipop.dropna(subset=['Position'])

        if not df_lollipop.empty:
            # Aggregate mutation counts by position
            mutation_counts = df_lollipop.groupby('Position').size().reset_index(name='Count')

            # Create Lollipop plot
            fig, ax = plt.subplots(figsize=(12, 3))
            ax.vlines(x=mutation_counts['Position'], ymin=0, ymax=mutation_counts['Count'],
                    colors='#1f77b4', linewidth=2)
            ax.plot(mutation_counts['Position'], mutation_counts['Count'], 'o', 
                    color='#ff7f0e', markersize=8)

            # Customize plot
            ax.set_xlabel('Amino Acid Position', fontsize=12)
            ax.set_ylabel('Variant Count', fontsize=12)
            ax.set_title(f'Lollipop Plot of Variants in {selected_gene}', fontsize=14)
            ax.grid(True, axis='y', linestyle='--', alpha=0.3)


            # X-axis: 0 to max position
            if selected_gene in SummaryViewerF1.GENE_LENGTHS:
                max_position = SummaryViewerF1.GENE_LENGTHS[selected_gene]
            else:
                max_position = mutation_counts['Position'].max() if mutation_counts['Position'].max() > 0 else mutation_counts['Position'].max() * (-5)
            mini_position = mutation_counts['Position'].min() if mutation_counts['Position'].min() < 0 else 0
            ax.set_xlim(mini_position * 1.1, max_position)
            
            # 100の倍数のラベル候補を作成
            start = ((mini_position + 99) // 100) * 100
            end = (max_position // 100) * 100
            xticks = np.arange(start, end + 1, 100)

            # 10個を超える場合は間引く
            if len(xticks) > 10:
                step = int(np.ceil(len(xticks) / 10))
                xticks = xticks[::step]

            # max_position を目盛りにだけ追加（ラベルなし）
            xticks_with_max = np.unique(np.append(xticks, max_position))  # 重複回避

            # ラベルの作成：max_positionは空白に
            xticklabels = [str(tick) if tick != max_position else '' for tick in xticks_with_max]

            ax.set_xticks(xticks_with_max)
            ax.set_xticklabels(xticklabels, fontsize=10)

            # Y-axis is integer count, so set it to integer format
            ax.yaxis.get_major_locator().set_params(integer=True)
            y_max = mutation_counts['Count'].max()
            ax.set_ylim(0, y_max * 1.1)  # Add 10% padding
            
            ax.spines['left'].set_position(('outward', 5))  # Move left spine to a small offset
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            # Display plot
            st.pyplot(fig)
        else:
            st.warning(f"No valid mutation data available for {selected_gene} with current filters.")
    else:
        st.info("Please select a gene from the sidebar to display the Lollipop plot.")
