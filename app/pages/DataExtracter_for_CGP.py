import streamlit as st
import pandas as pd
from io import BytesIO
import json
from annotator.parser import (
    parse_foundationone_xml, 
    parse_genminetop_xml, 
    parse_guardant360_excel,
    parse_hemesight_json,
    detect_xml_format, 
    detect_file_format
)

st.set_page_config(
    page_title="DataExtracter for CGP",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🧬 DataExtracter for CGP")

uploaded_files = st.sidebar.file_uploader(
    "Upload files", 
    type=["xml", "xlsx", "xls", "json"], 
    accept_multiple_files=True
)

# Remove duplicate files
if uploaded_files:
    seen_filenames = set()
    unique_files = []
    for file in uploaded_files:
        if file.name not in seen_filenames:
            unique_files.append(file)
            seen_filenames.add(file.name)
    st.success(f"{len(unique_files)} unique files have been uploaded.")
    uploaded_files = unique_files

if uploaded_files:
    # Unified data containers for all formats
    foundationone_data = {
        'sv': [], 'cna': [], 're': [], 'msi_tmb': [], 'nh': [], 'qc': []
    }
    genminetop_data = {
        'basic_info': [], 'sv': [], 'cna': [], 'fusions': [], 'expression': [], 'tmb': [], 'qc': []
    }
    guardant360_data = {
        'snv': [], 'indels': [], 'cna': [], 'fusions': [], 'msi': [], 'qc': []
    }
    hemesight_data = {
        'case': [], 'sv': [], 'rearrangement': [], 'fusions': [], 'sequencing': []
    }
    
    file_formats = {}
    processing_errors = []

    # Unified file processing loop
    for file in uploaded_files:
        try:
            if file.name.lower().endswith('.xml'):
                content = file.read().decode("utf-8")
                format_type = detect_xml_format(content)
                file_formats[file.name] = format_type
                
                if format_type == 'foundationone':
                    df_sv, df_cna, df_re, df_msi_tmb, df_nh, df_qc = parse_foundationone_xml(content)
                    foundationone_data['sv'].append(df_sv)
                    foundationone_data['cna'].append(df_cna)
                    foundationone_data['re'].append(df_re)
                    foundationone_data['msi_tmb'].append(df_msi_tmb)
                    foundationone_data['nh'].append(df_nh)
                    foundationone_data['qc'].append(df_qc)
                    
                elif format_type == 'genminetop':
                    df_basic_info, df_sv, df_cna, df_fusions, df_expression, df_tmb, df_qc = parse_genminetop_xml(content)
                    genminetop_data['basic_info'].append(df_basic_info)
                    genminetop_data['sv'].append(df_sv)
                    genminetop_data['cna'].append(df_cna)
                    genminetop_data['fusions'].append(df_fusions)
                    genminetop_data['expression'].append(df_expression)
                    genminetop_data['tmb'].append(df_tmb)
                    genminetop_data['qc'].append(df_qc)
                else:
                    file_formats[file.name] = 'unknown_xml'
                    
            elif file.name.lower().endswith(('.xlsx', '.xls')):
                content = file.read()
                format_type = detect_file_format(content, file.name)
                file_formats[file.name] = format_type
                
                if format_type == 'guardant360':
                    df_snv, df_indels, df_cna, df_fusions, df_msi, df_qc = parse_guardant360_excel(content, file.name)
                    guardant360_data['snv'].append(df_snv)
                    guardant360_data['indels'].append(df_indels)
                    guardant360_data['cna'].append(df_cna)
                    guardant360_data['fusions'].append(df_fusions)
                    guardant360_data['msi'].append(df_msi)
                    guardant360_data['qc'].append(df_qc)
                else:
                    file_formats[file.name] = 'unknown_excel'
                    
            elif file.name.lower().endswith('.json'):
                content = file.read()
                format_type = detect_file_format(content, file.name)
                file_formats[file.name] = format_type
                
                if format_type == 'hemesight':
                    json_data = json.loads(content)
                    df_case, df_short, df_rearrangement, df_sequencing = parse_hemesight_json(json_data)
                    hemesight_data['case'].append(df_case)
                    hemesight_data['sv'].append(df_short)
                    hemesight_data['rearrangement'].append(df_rearrangement)
                    hemesight_data['sequencing'].append(df_sequencing)
                else:
                    file_formats[file.name] = 'unknown_json'
            else:
                file_formats[file.name] = 'unsupported'
                
        except Exception as e:
            processing_errors.append(f"Error processing {file.name}: {str(e)}")
            file_formats[file.name] = 'error'

    # Display file format summary
    st.sidebar.write("### File Format Summary")
    for filename, fmt in file_formats.items():
        if fmt == 'foundationone':
            st.sidebar.write(f"🔬 {filename}: FoundationOne")
        elif fmt == 'genminetop':
            st.sidebar.write(f"🧪 {filename}: GenMineTOP")
        elif fmt == 'guardant360':
            st.sidebar.write(f"🩸 {filename}: Guardant360")
        elif fmt == 'hemesight':
            st.sidebar.write(f"🩸 {filename}: HemeSight")
        elif fmt == 'error':
            st.sidebar.write(f"❌ {filename}: Processing Error")
        else:
            st.sidebar.write(f"❓ {filename}: Unknown format")

    # Display processing errors if any
    if processing_errors:
        st.error("Processing Errors:")
        for error in processing_errors:
            st.error(error)

    # Process FoundationOne data
    foundationone_combined = {}
    if any(foundationone_data.values()):
        st.header("📊 FoundationOne Data")
        
        for key, data_list in foundationone_data.items():
            if data_list:
                foundationone_combined[key] = pd.concat(data_list, ignore_index=True)
            else:
                foundationone_combined[key] = pd.DataFrame()

        # Display FoundationOne tabs
        f1_tabs = st.tabs(["Short Variants", "Copy Number", "Rearrangements", "MSI/TMB", "Non-Human", "Quality Control"])
        with f1_tabs[0]: 
            if not foundationone_combined['sv'].empty:
                st.dataframe(foundationone_combined['sv'])
            else:
                st.info("No FoundationOne short variants data")
        with f1_tabs[1]: 
            if not foundationone_combined['cna'].empty:
                st.dataframe(foundationone_combined['cna'])
            else:
                st.info("No FoundationOne copy number data")
        with f1_tabs[2]: 
            if not foundationone_combined['re'].empty:
                st.dataframe(foundationone_combined['re'])
            else:
                st.info("No FoundationOne rearrangements data")
        with f1_tabs[3]: 
            if not foundationone_combined['msi_tmb'].empty:
                st.dataframe(foundationone_combined['msi_tmb'])
            else:
                st.info("No FoundationOne MSI/TMB data")
        with f1_tabs[4]: 
            if not foundationone_combined['nh'].empty:
                st.dataframe(foundationone_combined['nh'])
            else:
                st.info("No FoundationOne non-human data")
        with f1_tabs[5]: 
            if not foundationone_combined['qc'].empty:
                st.dataframe(foundationone_combined['qc'])
            else:
                st.info("No FoundationOne quality control data")

    # Process GenMineTOP data
    genminetop_combined = {}
    if any(genminetop_data.values()):
        st.header("🔬 GenMineTOP Data")
        
        for key, data_list in genminetop_data.items():
            if data_list:
                genminetop_combined[key] = pd.concat(data_list, ignore_index=True)
            else:
                genminetop_combined[key] = pd.DataFrame()

        # Display GenMineTOP tabs
        genminetop_tabs = st.tabs(["Basic Info", "Short Variants", "Copy Number", "Fusions", "Expression", "TMB/Signatures", "Quality Control"])
        with genminetop_tabs[0]: 
            if not genminetop_combined['basic_info'].empty:
                st.dataframe(genminetop_combined['basic_info'])
            else:
                st.info("No GenMineTOP short variants data")        
        with genminetop_tabs[1]: 
            if not genminetop_combined['sv'].empty:
                st.dataframe(genminetop_combined['sv'])
            else:
                st.info("No GenMineTOP short variants data")
        with genminetop_tabs[2]: 
            if not genminetop_combined['cna'].empty:
                st.dataframe(genminetop_combined['cna'])
            else:
                st.info("No GenMineTOP copy number data")
        with genminetop_tabs[3]: 
            if not genminetop_combined['fusions'].empty:
                st.dataframe(genminetop_combined['fusions'])
            else:
                st.info("No GenMineTOP fusions data")
        with genminetop_tabs[4]: 
            if not genminetop_combined['expression'].empty:
                st.dataframe(genminetop_combined['expression'])
            else:
                st.info("No GenMineTOP expression data")
        with genminetop_tabs[5]: 
            if not genminetop_combined['tmb'].empty:
                st.dataframe(genminetop_combined['tmb'])
            else:
                st.info("No GenMineTOP TMB data")
        with genminetop_tabs[6]: 
            if not genminetop_combined['qc'].empty:
                st.dataframe(genminetop_combined['qc'])
            else:
                st.info("No GenMineTOP quality control data")

    # Process Guardant360 data
    guardant360_combined = {}
    if any(guardant360_data.values()):
        st.header("🩸 Guardant360 Data")
        
        for key, data_list in guardant360_data.items():
            if data_list:
                guardant360_combined[key] = pd.concat(data_list, ignore_index=True)
            else:
                guardant360_combined[key] = pd.DataFrame()

        # Display Guardant360 tabs
        g360_tabs = st.tabs(["SNV", "Indels", "Copy Number", "Fusions", "MSI", "Quality Control"])
        with g360_tabs[0]: 
            if not guardant360_combined['snv'].empty:
                st.dataframe(guardant360_combined['snv'])
            else:
                st.info("No Guardant360 SNV data")
        with g360_tabs[1]: 
            if not guardant360_combined['indels'].empty:
                st.dataframe(guardant360_combined['indels'])
            else:
                st.info("No Guardant360 indels data")
        with g360_tabs[2]: 
            if not guardant360_combined['cna'].empty:
                st.dataframe(guardant360_combined['cna'])
            else:
                st.info("No Guardant360 copy number data")
        with g360_tabs[3]: 
            if not guardant360_combined['fusions'].empty:
                st.dataframe(guardant360_combined['fusions'])
            else:
                st.info("No Guardant360 fusions data")
        with g360_tabs[4]: 
            if not guardant360_combined['msi'].empty:
                st.dataframe(guardant360_combined['msi'])
            else:
                st.info("No Guardant360 MSI data")
        with g360_tabs[5]: 
            if not guardant360_combined['qc'].empty:
                st.dataframe(guardant360_combined['qc'])
            else:
                st.info("No Guardant360 quality control data")

    # Process HemeSight data
    hemesight_combined = {}
    if any(hemesight_data.values()):
        st.header("🧬 HemeSight Data")
        
        for key, data_list in hemesight_data.items():
            # data_listがリストで空でなければconcat、それ以外は空DataFrameをセット
            if isinstance(data_list, list) and len(data_list) > 0:
                hemesight_combined[key] = pd.concat(data_list, ignore_index=True)
            else:
                hemesight_combined[key] = pd.DataFrame()
        # Display HemeSight tabs
        hemesight_tabs = st.tabs(["Case Info", "Short Variants", "Rearrangements", "Sequencing"])
        with hemesight_tabs[0]: 
            if not hemesight_combined['case'].empty:
                st.dataframe(hemesight_combined['case'])
            else:
                st.info("No HemeSight case data")        
        with hemesight_tabs[1]: 
            if not hemesight_combined['sv'].empty:
                st.dataframe(hemesight_combined['sv'])
            else:
                st.info("No HemeSight short variants data")
        with hemesight_tabs[2]: 
            if 'rearrangement' in hemesight_combined and not hemesight_combined['rearrangement'].empty:
                st.dataframe(hemesight_combined['rearrangement'])
            else:
                st.info("No HemeSight rearrangements data")
        with hemesight_tabs[3]: 
            if not hemesight_combined['sequencing'].empty:
                st.dataframe(hemesight_combined['sequencing'])
            else:
                st.info("No HemeSight sequencing data")


    # Excel export section
    st.header("💾 Export Data")
    
    # Create Excel file with all data
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # FoundationOne data
        if any(foundationone_data.values()):
            if not foundationone_combined['sv'].empty:
                foundationone_combined['sv'].to_excel(writer, index=False, sheet_name='F1_ShortVariants')
            if not foundationone_combined['cna'].empty:
                foundationone_combined['cna'].to_excel(writer, index=False, sheet_name='F1_CopyNumber')
            if not foundationone_combined['re'].empty:
                foundationone_combined['re'].to_excel(writer, index=False, sheet_name='F1_Rearrangements')
            if not foundationone_combined['msi_tmb'].empty:
                foundationone_combined['msi_tmb'].to_excel(writer, index=False, sheet_name='F1_MSI_TMB')
            if not foundationone_combined['nh'].empty:
                foundationone_combined['nh'].to_excel(writer, index=False, sheet_name='F1_NonHuman')
            if not foundationone_combined['qc'].empty:
                foundationone_combined['qc'].to_excel(writer, index=False, sheet_name='F1_QualityControl')
        
        # GenMineTOP data
        if any(genminetop_data.values()):
            if not genminetop_combined['sv'].empty:
                genminetop_combined['sv'].to_excel(writer, index=False, sheet_name='GenMineTOP_ShortVariants')
            if not genminetop_combined['cna'].empty:
                genminetop_combined['cna'].to_excel(writer, index=False, sheet_name='GenMineTOP_CopyNumber')
            if not genminetop_combined['fusions'].empty:
                genminetop_combined['fusions'].to_excel(writer, index=False, sheet_name='GenMineTOP_Fusions')
            if not genminetop_combined['expression'].empty:
                genminetop_combined['expression'].to_excel(writer, index=False, sheet_name='GenMineTOP_Expression')
            if not genminetop_combined['tmb'].empty:
                genminetop_combined['tmb'].to_excel(writer, index=False, sheet_name='GenMineTOP_TMB')
            if not genminetop_combined['qc'].empty:
                genminetop_combined['qc'].to_excel(writer, index=False, sheet_name='GenMineTOP_QualityControl')
        
        # Guardant360 data
        if any(guardant360_data.values()):
            if not guardant360_combined['snv'].empty:
                guardant360_combined['snv'].to_excel(writer, index=False, sheet_name='Guardant360_SNV')
            if not guardant360_combined['indels'].empty:
                guardant360_combined['indels'].to_excel(writer, index=False, sheet_name='Guardant360_Indels')
            if not guardant360_combined['cna'].empty:
                guardant360_combined['cna'].to_excel(writer, index=False, sheet_name='Guardant360_CopyNumber')
            if not guardant360_combined['fusions'].empty:
                guardant360_combined['fusions'].to_excel(writer, index=False, sheet_name='Guardant360_Fusions')
            if not guardant360_combined['msi'].empty:
                guardant360_combined['msi'].to_excel(writer, index=False, sheet_name='Guardant360_MSI')
            if not guardant360_combined['qc'].empty:
                guardant360_combined['qc'].to_excel(writer, index=False, sheet_name='Guardant360_QualityControl')
        
        # HemeSight data
        if any(hemesight_data.values()):
            if not hemesight_combined['case'].empty:
                hemesight_combined['case'].to_excel(writer, index=False, sheet_name='HemeSight_CaseInfo')
            if not hemesight_combined['sv'].empty:
                hemesight_combined['sv'].to_excel(writer, index=False, sheet_name='HemeSight_ShortVariants')
            if not hemesight_combined['rearrangement'].empty:
                hemesight_combined['rearrangement'].to_excel(writer, index=False, sheet_name='HemeSight_Rearrangements')
            if not hemesight_combined['sequencing'].empty:
                hemesight_combined['sequencing'].to_excel(writer, index=False, sheet_name='HemeSight_Sequencing')
                
        # File format summary
        format_summary = pd.DataFrame([
            {'Filename': filename, 'Format': fmt} 
            for filename, fmt in file_formats.items()
        ])
        format_summary.to_excel(writer, index=False, sheet_name='File_Formats')
    
    output.seek(0)

    st.download_button(
        label="⬇️ Save in Excel format (all sheets)",
        data=output,
        file_name="cgp_extraction_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Summary statistics
    st.header("📈 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if any(foundationone_data.values()):
            st.metric("FoundationOne Files", len([f for f, fmt in file_formats.items() if fmt == 'foundationone']))
            if not foundationone_combined['sv'].empty:
                st.metric("F1 Short Variants", len(foundationone_combined['sv']))
            if not foundationone_combined['cna'].empty:
                st.metric("F1 Copy Number", len(foundationone_combined['cna']))
    
    with col2:
        if any(genminetop_data.values()):
            st.metric("GenMineTOP Files", len([f for f, fmt in file_formats.items() if fmt == 'genminetop']))
            if not genminetop_combined['sv'].empty:
                st.metric("GenMineTOP Variants", len(genminetop_combined['sv']))
            if not genminetop_combined['fusions'].empty:
                st.metric("GenMineTOP Fusions", len(genminetop_combined['fusions']))
    
    with col3:
        if any(guardant360_data.values()):
            st.metric("Guardant360 Files", len([f for f, fmt in file_formats.items() if fmt == 'guardant360']))
            if not guardant360_combined['snv'].empty:
                st.metric("G360 SNVs", len(guardant360_combined['snv']))
            if not guardant360_combined['indels'].empty:
                st.metric("G360 Indels", len(guardant360_combined['indels']))
    
    with col4:
        if any(hemesight_data.values()):
            st.metric("HemeSight Files", len([f for f, fmt in file_formats.items() if fmt == 'hemesight']))
            if not hemesight_combined['sv'].empty:
                st.metric("HemeSight Variants", len(hemesight_combined['sv']))