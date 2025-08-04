import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl
import io
import tarfile
import gzip
import tempfile
import os
from pathlib import Path
import zipfile

def extract_compressed_file(uploaded_file):
    """
    圧縮ファイルを展開し、含まれるファイルのリストを返す
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        file_content = uploaded_file.read()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        extracted_files = []

        # ZIPファイルの処理
        if uploaded_file.name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                for member in zip_ref.infolist():
                    if not member.is_dir():
                        file_ext = Path(member.filename).suffix.lower()
                        if file_ext in ['.csv', '.tsv', '.xlsx', '.xls', '.txt', '.vcf']:
                            with open(os.path.join(temp_dir, member.filename), 'rb') as f:
                                extracted_files.append({
                                    'name': member.filename,
                                    'content': f.read()
                                })

        elif uploaded_file.name.endswith('.tar.gz') or uploaded_file.name.endswith('.tgz'):
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(temp_dir)
                for member in tar.getmembers():
                    if member.isfile():
                        file_ext = Path(member.name).suffix.lower()
                        if file_ext in ['.csv', '.tsv', '.xlsx', '.xls', '.txt', '.vcf']:
                            with open(os.path.join(temp_dir, member.name), 'rb') as f:
                                extracted_files.append({
                                    'name': member.name,
                                    'content': f.read()
                                })

        elif uploaded_file.name.endswith('.gz'):
            with gzip.open(file_path, 'rb') as gz:
                content = gz.read()
                original_name = uploaded_file.name[:-3]
                file_ext = Path(original_name).suffix.lower()
                if file_ext in ['.csv', '.tsv', '.xlsx', '.xls', '.txt', '.vcf']:
                    extracted_files.append({
                        'name': original_name,
                        'content': content
                    })
        
        return extracted_files


def read_vcf(file, encoding='utf-8', skiprows=0):
    """
    VCFファイルを読み込んでDataFrameに変換する関数
    """
    # ファイルを文字列として読み込む
    content = file.read().decode(encoding)
    
    # メタデータとヘッダー行を処理
    headers = []
    data = []
    meta_info = {}
    
    lines = content.split('\n')
    line_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:  # 空行をスキップ
            continue
            
        if line.startswith('##'):
            # メタデータの処理
            if '=' in line:
                key = line[2:].split('=')[0]
                value = '='.join(line[2:].split('=')[1:])
                meta_info[key] = value
            continue
            
        if line.startswith('#'):
            # ヘッダー行の処理
            if line_count >= skiprows:
                headers = line[1:].split('\t')
            continue
            
        # データ行の処理
        if headers and line and line_count >= skiprows:
            row = line.split('\t')
            if len(row) == len(headers):
                data.append(row)
        line_count += 1
    
    # DataFrameの作成
    if headers and data:
        df = pd.DataFrame(data, columns=headers)
        return df, meta_info
    else:
        return pd.DataFrame(), {}

# ページ設定
st.set_page_config(
    page_title="🔎 DataViewer",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",    
)

# タイトルとサブタイトル
st.title("🔎 DataViewer")
st.markdown("Upload your CSV, TSV, TXT, VCF, Excel file, or compressed (tar.gz, gz) files")

# サイドバーの設定
with st.sidebar:
    st.header("Settings")
    
    # ファイルのアップロード（圧縮ファイルのサポートを追加）
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["csv", "tsv", "xlsx", "xls", "txt", "vcf", "tar.gz", "tgz", "gz", "zip"]
    )
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        # 圧縮ファイルの場合、含まれるファイルを展開してリスト表示
        if file_type in ['gz', 'tgz', 'zip'] or uploaded_file.name.endswith('.tar.gz'):
            extracted_files = extract_compressed_file(uploaded_file)
            if extracted_files:
                selected_file = st.selectbox(
                    "Select file to analyze:",
                    options=[f['name'] for f in extracted_files],
                    format_func=lambda x: os.path.basename(x)
                )
                # 選択されたファイルの内容をメモリ上のファイルとして扱う
                selected_content = next(f['content'] for f in extracted_files if f['name'] == selected_file)
                uploaded_file = io.BytesIO(selected_content)
                uploaded_file.name = selected_file
                file_type = selected_file.split('.')[-1].lower()
            else:
                st.error("No supported files found in the compressed archive")
                st.stop()

        
        # タイトル行の設定
        st.subheader("Header Settings")
        header_row = st.number_input("Header row number (0-based)", min_value=0, value=0)
        
        if file_type in ['csv', 'tsv', 'txt', 'vcf']:
            # CSVとTSV用の設定
            st.subheader("CSV/TSV/VCF Settings")
            encoding_option = st.selectbox(
                "Select file encoding",
                options=["utf-8", "shift-jis", "cp932", "utf-16"],
                index=0
            )
            
            if file_type != 'vcf':
                delimiter_option = st.selectbox(
                    "Select delimiter",
                    options=[",", "\t", ";", "|"],
                    index=0 if file_type == 'csv' else 1,
                    format_func=lambda x: "Tab" if x == "\t" else x
                )
            else:
                delimiter_option = "\t"
            
            error_bad_lines = st.checkbox("Skip problematic lines", value=True)
            
            if error_bad_lines:
                st.info("Lines with incorrect number of fields will be skipped")
        
        elif file_type in ['xlsx', 'xls']:
            # Excel用の設定
            st.subheader("Excel Settings")
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            selected_sheet = st.selectbox(
                "Select sheet",
                options=sheet_names
            )


if uploaded_file is not None:
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'vcf':
            # VCFファイルの読み込み
            df, meta_info = read_vcf(uploaded_file, encoding=encoding_option, skiprows=header_row)
            
            # メタ情報の表示
            if meta_info:
                st.subheader("VCF Meta Information")
                meta_df = pd.DataFrame(list(meta_info.items()), columns=['Key', 'Value'])
                st.dataframe(meta_df)
                
        elif file_type in ['csv', 'tsv', 'txt']:
            # CSVファイルの読み込み
            df = pd.read_csv(
                uploaded_file,
                encoding=encoding_option,
                delimiter=delimiter_option,
                on_bad_lines='warn' if error_bad_lines else 'error',
                header=header_row
            )
        else:
            # Excelファイルの読み込み
            df = pd.read_excel(
                uploaded_file,
                sheet_name=selected_sheet,
                header=header_row
            )

        # 読み込み結果の表示
        st.success(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        
        # 基本情報の表示
        st.header("Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isna().sum().sum())
        with col4:
            st.metric("Duplicate Rows", df.duplicated().sum())
        
        # 列情報の表示
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            'Type': df.dtypes,
            'Non-Null Count': df.count(),
            'Null Count': df.isna().sum(),
            'Unique Values': df.nunique()
        })
        st.dataframe(col_info)
        
        # データプレビュー
        st.header("Preview")
        st.dataframe(df)
        
# データ分析セクション
        st.header("Analysis")
        
        # 検索機能
        st.subheader("Search Data")
        search_col, filter_col = st.columns(2)
        with search_col:
            search_text = st.text_input("Enter search terms (separate by comma or space):")
            search_mode = st.radio(
                "Search mode:",
                ["Match any term (OR)", "Match all terms (AND)"],
                horizontal=True
            )
        with filter_col:
            selected_columns = st.multiselect(
                "Select columns to search in:",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )
        
        # 検索結果のデータフレームを初期化
        filtered_df = df.copy()
        
        if search_text:
            # 検索語を分割（カンマまたはスペースで区切る）
            search_terms = [term.strip() for term in search_text.replace(',', ' ').split()]
            
            if search_terms:
                if search_mode == "Match any term (OR)":
                    # いずれかの検索語にマッチ（OR検索）
                    masks = []
                    for term in search_terms:
                        mask = df[selected_columns].astype(str).apply(
                            lambda x: x.str.contains(term, case=False)
                        ).any(axis=1)
                        masks.append(mask)
                    final_mask = pd.concat(masks, axis=1).any(axis=1)
                else:
                    # すべての検索語にマッチ（AND検索）
                    masks = []
                    for term in search_terms:
                        mask = df[selected_columns].astype(str).apply(
                            lambda x: x.str.contains(term, case=False)
                        ).any(axis=1)
                        masks.append(mask)
                    final_mask = pd.concat(masks, axis=1).all(axis=1)
                
                filtered_df = df[final_mask]
                
                # 検索結果の表示
                st.write(f"Found {len(filtered_df)} matching rows")
                if len(filtered_df) > 0:
                    st.write("Search terms found in:")
                    for term in search_terms:
                        term_matches = []
                        for col in selected_columns:
                            matches = filtered_df[filtered_df[col].astype(str).str.contains(term, case=False)][col].unique()
                            if len(matches) > 0:
                                term_matches.append(f"{col} ({len(matches)} unique values)")
                        if term_matches:
                            st.write(f"- '{term}': {', '.join(term_matches)}")
                
                st.dataframe(filtered_df)
        
        # 全ての列を対象にする（数値列に限定しない）
        all_cols = filtered_df.columns.tolist()
        
        if len(all_cols) > 0:
            # 基本統計量（数値列のみ）
            numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                st.subheader("Statistical Summary")
                st.dataframe(filtered_df[numeric_cols].describe())
            
            # グラフ作成
            st.subheader("Visualization")
            chart_type = st.selectbox(
                "Select chart type:",
                ["Histogram", "Box Plot", "Violin Plot", "Scatter Plot", "Stacked Bar Chart"]
            )
            
            if chart_type == "Histogram":
                col = st.selectbox("Select column for histogram:", all_cols)
                
                # 選択された列の型に応じて適切な処理を行う
                if filtered_df[col].dtype in ['int64', 'float64']:
                    # 数値データの場合は通常のヒストグラム
                    fig = px.histogram(filtered_df, x=col)
                else:
                    # 文字列データの場合は度数分布図
                    value_counts = filtered_df[col].value_counts()
                    fig = px.bar(x=value_counts.index, 
                               y=value_counts.values,
                               labels={'x': col, 'y': 'Count'},
                               title=f'Distribution of {col}')
                
                # グラフの表示オプション
                show_options = st.expander("Show graph options", expanded=False)
                with show_options:
                    # 並び替えオプション（文字列データの場合のみ）
                    if filtered_df[col].dtype not in ['int64', 'float64']:
                        sort_order = st.selectbox(
                            "Sort order:",
                            ["Value (Ascending)", "Value (Descending)", 
                             "Frequency (Ascending)", "Frequency (Descending)"]
                        )
                        
                        if sort_order == "Value (Ascending)":
                            value_counts = value_counts.sort_index()
                        elif sort_order == "Value (Descending)":
                            value_counts = value_counts.sort_index(ascending=False)
                        elif sort_order == "Frequency (Ascending)":
                            value_counts = value_counts.sort_values()
                        else:  # Frequency (Descending)
                            value_counts = value_counts.sort_values(ascending=False)
                        
                        # 更新されたデータでグラフを再描画
                        fig = px.bar(x=value_counts.index, 
                                   y=value_counts.values,
                                   labels={'x': col, 'y': 'Count'},
                                   title=f'Distribution of {col}')
                    
                    # 表示件数の制限（文字列データの場合のみ）
                    if filtered_df[col].dtype not in ['int64', 'float64']:
                        max_items = st.slider(
                            "Maximum number of items to display:",
                            min_value=1,  # Changed from 5 to 1
                            max_value=max(1, min(50, len(value_counts))),  # Added max(1, ...) to ensure it's never less than 1
                            value=min(20, len(value_counts))
                        )
                        value_counts = value_counts.head(max_items)
                        
                        # 更新されたデータでグラフを再描画
                        fig = px.bar(x=value_counts.index, 
                                   y=value_counts.values,
                                   labels={'x': col, 'y': 'Count'},
                                   title=f'Distribution of {col} (Top {max_items} items)')
                    
                    # グラフの回転オプション（文字列データの場合のみ）
                    if filtered_df[col].dtype not in ['int64', 'float64']:
                        rotate_labels = st.checkbox("Rotate x-axis labels", value=False)
                        if rotate_labels:
                            fig.update_layout(xaxis_tickangle=-45)

                st.plotly_chart(fig)
                
            elif chart_type == "Box Plot":
                col = st.selectbox("Select column for box plot:", numeric_cols)
                group = st.selectbox("Group by column (optional):", ["None"] + all_cols, key="boxplot_group")
                if group == "None":
                    fig = px.box(filtered_df, y=col)
                else:
                    fig = px.box(filtered_df, x=group, y=col)
                st.plotly_chart(fig)
                
            elif chart_type == "Violin Plot":
                col = st.selectbox("Select column for violin plot:", numeric_cols)
                group = st.selectbox("Group by column (optional):", ["None"] + all_cols, key="violinplot_group")
                if group == "None":
                    fig = px.violin(filtered_df, y=col)
                else:
                    fig = px.violin(filtered_df, x=group, y=col)
                st.plotly_chart(fig)
            
            elif chart_type == "Scatter Plot":
                col_x = st.selectbox("Select X axis:", numeric_cols)
                col_y = st.selectbox("Select Y axis:", numeric_cols)
                fig = px.scatter(filtered_df, x=col_x, y=col_y)
                st.plotly_chart(fig)
                
            elif chart_type == "Stacked Bar Chart":
                col_x = st.selectbox("Select X axis:", all_cols)
                col_y = st.selectbox("Select Y axis:", all_cols)
                fig = px.bar(filtered_df, x=col_x, y=col_y, color=col_y)
                st.plotly_chart(fig)

    except UnicodeDecodeError:
        st.error("Error reading the file. Try a different encoding from the sidebar.")
        st.info("Common encodings for Japanese files are 'shift-jis' or 'cp932'")
    except pd.errors.ParserError as e:
        st.error("Error parsing the CSV/TSV file:")
        st.error(str(e))
        st.info("Try selecting a different delimiter or enable 'Skip problematic lines' in the sidebar")
    except Exception as e:
        st.error("An unexpected error occurred:")
        st.error(str(e))

else:
    st.info("Please upload a CSV, TSV, TXT, VCF, or Excel file to begin analysis.")