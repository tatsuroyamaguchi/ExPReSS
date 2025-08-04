import xml.etree.ElementTree as ET
import pandas as pd
from typing import Tuple, Union
import re

def parse_foundationone_xml(xml_content: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ns = {
        'rr': 'http://integration.foundationmedicine.com/reporting',
        'vr': 'http://foundationmedicine.com/compbio/variant-report-external'
    }

    root = ET.fromstring(xml_content)
    report = root.find('.//vr:variant-report', namespaces=ns)

    ref_id = root.findtext('.//rr:ReferenceID', namespaces=ns)
    disease = report.attrib.get('disease', '')
    gender = report.attrib.get('gender', '')
    sample = report.find('.//vr:samples/vr:sample', namespaces=ns).attrib.get('name', '')

    # short variants
    short_variants = []
    for sv in root.findall('.//vr:short-variant', namespaces=ns):
        short_variants.append({
            'ReferenceID': ref_id,
            'Gender': gender,
            'Disease': disease,
            'Gene': sv.attrib.get('gene'),
            'Position': sv.attrib.get('position'),
            'Transcript': sv.attrib.get('transcript'),
            'CDS_Effect': sv.attrib.get('cds-effect'),
            'Protein_Effect': sv.attrib.get('protein-effect'),
            'Functional_Effect': sv.attrib.get('functional-effect'),
            'Allele_Fraction': sv.attrib.get('allele-fraction'),
            'Depth': sv.attrib.get('depth'),
            'Status': sv.attrib.get('status'),
        })
    df_sv = pd.DataFrame(short_variants)

    # CNAs
    cna = []
    for cn in root.findall('.//vr:copy-number-alteration', namespaces=ns):
        cna.append({
            'ReferenceID': ref_id,
            'Gender': gender,
            'Disease': disease,
            'Gene': cn.attrib.get('gene'),
            'Position': cn.attrib.get('position'),
            'CopyNumber': cn.attrib.get('copy-number'),
            'Ratio': cn.attrib.get('ratio'),
            'Type': cn.attrib.get('type'),
            'Status': cn.attrib.get('status'),
        })
    df_cna = pd.DataFrame(cna)

    # Rearrangements
    re_list = []
    for re in root.findall('.//vr:rearrangement', namespaces=ns):
        re_list.append({
            'ReferenceID': ref_id,
            'Gender': gender,
            'Disease': disease,
            'TargetedGene': re.attrib.get('targeted-gene'),
            'OtherGene': re.attrib.get('other-gene'),
            'Description': re.attrib.get('description'),
            'Type': re.attrib.get('type'),
            'Allele_Fraction': re.attrib.get('allele-fraction'),
            'Percent_Reads': re.attrib.get('percent-reads'),
            'Supporting_Read_Pairs': re.attrib.get('supporting-read-pairs'),
            'Status': re.attrib.get('status'),
        })
    df_re = pd.DataFrame(re_list)

    # MSI / TMB
    biomarkers = root.find('.//vr:biomarkers', namespaces=ns)
    msi_status = biomarkers.find('.//vr:microsatellite-instability', namespaces=ns).attrib.get('status', '')
    tmb_elem = biomarkers.find('.//vr:tumor-mutation-burden', namespaces=ns)
    tmb_score = tmb_elem.attrib.get('score', '')
    tmb_status = tmb_elem.attrib.get('status', '')
    tmb_unit = tmb_elem.attrib.get('unit', '')

    df_msi_tmb = pd.DataFrame([{
        'ReferenceID': ref_id,
        'Gender': gender,
        'Disease': disease,
        'MSI_Status': msi_status,
        'TMB_Score': tmb_score,
        'TMB_Status': tmb_status,
    }])

    # Non-human content
    non_human_list = []
    for nh in root.findall('.//vr:non-human', namespaces=ns):
        non_human_list.append({
            'ReferenceID': ref_id,
            'Gender': gender,
            'Disease': disease,
            'Organism': nh.attrib.get('organism'),
            'ReadsPerMillion': nh.attrib.get('reads-per-million'),
            'Status': nh.attrib.get('status'),
        })
    df_nh = pd.DataFrame(non_human_list)

    # Quality control
    qc_elem = report.find('.//vr:quality-control', namespaces=ns)
    qc_status = qc_elem.attrib.get('status', '') if qc_elem is not None else ''
    df_qc = pd.DataFrame([{
        'ReferenceID': ref_id,
        'Gender': gender,
        'Disease': disease,
        'QC_Status': qc_status,
    }])

    return df_sv, df_cna, df_re, df_msi_tmb, df_nh, df_qc

def parse_genminetop_xml(xml_content: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse GenMineTOP XML format
    Returns: short_variants, copy_number_alterations, fusions, expression, tmb, quality_control
    """
    root = ET.fromstring(xml_content)
    
    # Extract basic information
    report_id = root.findtext('.//id')
    patient_sex = root.findtext('.//patient/sex')
    patient_age = root.findtext('.//patient/age')
    c_cat_id = root.findtext('.//patient/c-cat-id')
    pathology = root.findtext('.//specimen/pathology')
    hospital = root.findtext('.//owner/hospital')
    
    # Basic information DataFrame
    basic_info = []
    basic_info.append({
        'ReportID': report_id,
        'Sex': patient_sex,
        'Age': patient_age,
        'C_CAT_ID': c_cat_id,
        'Pathology': pathology,
        'Hospital': hospital,
    })
    
    df_basic_info = pd.DataFrame(basic_info)
    
    # Short Variants (SNVs, Insertions, Deletions)
    short_variants = []
    for item in root.findall('.//alterations/item'):
        variant_type = item.findtext('type')
        if variant_type in ['snv', 'insertion', 'deletion']:
            gene_elem = item.find('gene')
            gene = gene_elem.text if gene_elem is not None else ''
            
            short_variants.append({
                'ReportID': report_id,
                'Gene': gene,
                'Transcript': item.findtext('transcript'),
                'Locus': item.findtext('locus'),
                'Ref': item.findtext('ref'),
                'Alt': item.findtext('alt'),
                'Cytoband': item.findtext('cytoband'),
                'Origin': item.findtext('origin'),
                'Type': variant_type,
                'CDS_Effect': item.findtext('coding-dna-alteration'),
                'Protein_Effect': item.findtext('protein-alteration'),
                'Allele_Frequency': item.findtext('allele-frequency'),
                'Status': item.findtext('status'),
                'AG_Class': item.findtext('ag-class'),
                'ClinVar_ID': item.findtext('.//clinvar/id/item'),
                'COSMIC_ID': item.findtext('.//cosmic/id/item'),
                'Clinical_Significance': item.findtext('.//clinical-significance/item'),
            })
    
    df_sv = pd.DataFrame(short_variants)
    
    # Copy Number Alterations
    cna_list = []
    for item in root.findall('.//alterations/item'):
        variant_type = item.findtext('type')
        if variant_type in ['cnv-amplification', 'cnv-deletion']:
            gene_elem = item.find('gene')
            gene = gene_elem.text if gene_elem is not None else ''
            
            cna_list.append({
                'ReportID': report_id,
                'Gene': gene,
                'Transcript': item.findtext('transcript'),
                'Locus': item.findtext('locus'),
                'Cytoband': item.findtext('cytoband'),
                'Origin': item.findtext('origin'),
                'Type': variant_type,
                'Copy_Number': item.findtext('num-copy'),
                'Ratio': item.findtext('ratio'),
                'Status': item.findtext('status'),
            })
    
    df_cna = pd.DataFrame(cna_list)
    
    # Fusions/Rearrangements
    fusions = []
    for item in root.findall('.//alterations/item'):
        variant_type = item.findtext('type')
        if variant_type == 'fusion':
            gene_elem = item.find('gene')
            if gene_elem is not None:
                # Handle multiple genes in fusion
                genes = [g.text for g in gene_elem.findall('item')] if gene_elem.findall('item') else [gene_elem.text]
                gene_str = ' - '.join(genes) if genes else ''
            else:
                gene_str = ''
                
            fusions.append({
                'ReportID': report_id,
                'Genes': gene_str,
                'Transcript': ' - '.join([t.text for t in item.findall('.//transcript/item')]),
                'Locus': ' - '.join([l.text for l in item.findall('.//locus/item')]),
                'Cytoband': ' - '.join([c.text for c in item.findall('.//cytoband/item')]),
                'Origin': item.findtext('origin'),
                'Type': variant_type,
                'Num_Reads': item.findtext('num-reads'),
                'Frame': item.findtext('frame'),
                'Status': item.findtext('status'),
                'Vendor_ID': item.findtext('.//id/vendor'),
            })
    
    df_fusions = pd.DataFrame(fusions)
    
    # Gene Expression (keeping separately as it's substantial data)
    expression_list = []
    for item in root.findall('.//alterations/item'):
        variant_type = item.findtext('type')
        if variant_type == 'expression':
            gene_elem = item.find('gene')
            gene = gene_elem.text if gene_elem is not None else ''
            
            expression_list.append({
                'ReportID': report_id,
                'Gene': gene,
                'Transcript': item.findtext('.//transcript/item'),
                'Origin': item.findtext('origin'),
                'Type': variant_type,
                'Num_Reads': item.findtext('num-reads'),
                'TPM': item.findtext('tpm'),
                'Normal_Mean_TPM': item.findtext('.//normal-expression/tpm/mean'),
                'Normal_SD_TPM': item.findtext('.//normal-expression/tpm/sd'),
                'Normal_N': item.findtext('.//normal-expression/tpm/n'),
                'Status': item.findtext('status'),
            })
    
    df_expression = pd.DataFrame(expression_list)
    
    # TMB and Mutational Signatures
    tmb_elem = root.find('.//marker/tmb/exon')
    signature_values = [int(item.text) for item in root.findall('.//marker/signature/values/item')]
    
    tmb_data = {
        'ReportID': report_id,
        'TMB_Non_Synonymous': tmb_elem.findtext('num-non-synonymous-alterations') if tmb_elem is not None else '',
        'TMB_Frequency': tmb_elem.findtext('frequency-non-synonymous-alterations') if tmb_elem is not None else '',
        'Signature_Values': ','.join(map(str, signature_values)),
    }
    
    df_tmb = pd.DataFrame([tmb_data])
    
    # Quality Control
    qc_data = []
    
    # Tumor content
    tumor_content_elem = root.find('.//qc/tumor-content')
    estimated_purity = tumor_content_elem.findtext('.//estimated/value') if tumor_content_elem is not None else ''
    nuclei_purity = tumor_content_elem.findtext('.//nuclei/value') if tumor_content_elem is not None else ''
    
    # Sequencing QC for DNA
    normal_dna = root.find('.//qc/sequence/normal/dna')
    tumor_dna = root.find('.//qc/sequence/tumor/dna')
    tumor_rna = root.find('.//qc/sequence/tumor/rna')
    
    qc_data.append({
        'ReportID': report_id,
        'Estimated_Tumor_Purity': estimated_purity,
        'Nuclei_Tumor_Purity': nuclei_purity,
        'Normal_DNA_Mean_Depth': normal_dna.findtext('.//mean-depth/value') if normal_dna is not None else '',
        'Normal_DNA_Status': normal_dna.findtext('status') if normal_dna is not None else '',
        'Tumor_DNA_Mean_Depth': tumor_dna.findtext('.//mean-depth/value') if tumor_dna is not None else '',
        'Tumor_DNA_Status': tumor_dna.findtext('status') if tumor_dna is not None else '',
        'Tumor_RNA_Total_Reads': tumor_rna.findtext('.//num-total-reads/value') if tumor_rna is not None else '',
        'Tumor_RNA_Status': tumor_rna.findtext('status') if tumor_rna is not None else '',
        'SNP_Correlation': root.findtext('.//qc/sequence/snp-correlation/value'),
    })
    
    df_qc = pd.DataFrame(qc_data)
    
    return df_basic_info, df_sv, df_cna, df_fusions, df_expression, df_tmb, df_qc

def parse_guardant360_excel(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse Guardant360 Excel format (Interim files)
    Returns: short_variants, indels, copy_number_alterations, fusions, msi, quality_control
    """
    # Extract sample ID from filename
    sample_id_match = re.search(r'Interim_(\d+)_(\d+)', filename)
    sample_id = sample_id_match.group(1) if sample_id_match else filename
    report_id = sample_id_match.group(2) if sample_id_match else ''
    
    try:
        # Read all sheets
        excel_data = pd.read_excel(file_content, sheet_name=None, engine='openpyxl')
        
        # SNV data
        df_snv = pd.DataFrame()
        if 'SNV' in excel_data:
            snv_data = excel_data['SNV'].copy()
            if not snv_data.empty:
                snv_data['SampleID'] = sample_id
                df_snv = snv_data
                df_snv = df_snv[['SampleID'] + [col for col in df_snv.columns if col != 'SampleID']]
        
        # Indels data
        df_indels = pd.DataFrame()
        if 'Indels' in excel_data:
            indels_data = excel_data['Indels'].copy()
            if not indels_data.empty:
                indels_data['SampleID'] = sample_id
                df_indels = indels_data
                df_indels = df_indels[['SampleID'] + [col for col in df_indels.columns if col != 'SampleID']]
        
        # CNAs data
        df_cna = pd.DataFrame()
        if 'CNAs' in excel_data:
            cna_data = excel_data['CNAs'].copy()
            if not cna_data.empty:
                cna_data['SampleID'] = sample_id
                df_cna = cna_data
                df_cna = df_cna[['SampleID'] + [col for col in df_cna.columns if col != 'SampleID']]
        
        # Fusions data
        df_fusions = pd.DataFrame()
        if 'Fusions' in excel_data:
            fusions_data = excel_data['Fusions'].copy()
            if not fusions_data.empty:
                fusions_data['SampleID'] = sample_id
                df_fusions = fusions_data
                df_fusions = df_fusions[['SampleID'] + [col for col in df_fusions.columns if col != 'SampleID']]
        
        # MSI data
        df_msi = pd.DataFrame()
        if 'MSI' in excel_data:
            msi_data = excel_data['MSI'].copy()
            if not msi_data.empty:
                msi_data['SampleID'] = sample_id
                df_msi = msi_data
                df_msi = df_msi[['SampleID'] + [col for col in df_msi.columns if col != 'SampleID']]
                df_msi.drop(columns=['runid'], inplace=True)
                df_msi.drop(columns=['run_sample_id'], inplace=True)
        
        # QC data
        df_qc = pd.DataFrame()
        if 'QC' in excel_data:
            qc_data = excel_data['QC'].copy()
            if not qc_data.empty:
                qc_data['SampleID'] = sample_id
                df_qc = qc_data
                df_qc = df_qc[['SampleID'] + [col for col in df_qc.columns if col != 'SampleID']]
        
        return df_snv, df_indels, df_cna, df_fusions, df_msi, df_qc
        
    except Exception as e:
        print(f"Error parsing Guardant360 file {filename}: {str(e)}")
        # Return empty DataFrames with proper columns
        empty_df = pd.DataFrame()
        return empty_df, empty_df, empty_df, empty_df, empty_df, empty_df

def parse_hemesight_json(json_data: dict, output_excel: str = "parsed_hemesight_variants.xlsx") -> None:
    """
    Parse shortVariants, rearrangements, and fusion sections of Hemsight JSON data
    and save them to separate sheets in an Excel file.
    
    Args:
        json_data (dict): The JSON data as a dictionary.
        output_excel (str): Path to the output Excel file.
    """
    # Initialize lists for each variant type
    case_info = []
    short_variant_records = []
    rearrangement_records = []
    sequencing_saples = []
    
    # Extract case information
    case_data = json_data.get("caseData", {})
    case_info.append({
        "CaseID": case_data.get("caseId", ""),
        "CancerClassification": case_data.get("cancerClassification", ""),
        "CancerType": case_data.get("cancerType", ""),
        "HsctHistory": case_data.get("hsctHistory", ""),
        "GermlineFindingsDisclosure": case_data.get("germlineFindingsDisclosure", "")
    })

    # Parse shortVariants
    short_variants = json_data.get("variants", {}).get("shortVariants", [])
    for var in short_variants:
        for transcript in var.get("transcripts", []):
            short_variant_records.append({
                "CaseID": case_data.get("caseId", ""),
                "ItemID": var.get("itemId"),
                "Gene": transcript.get("geneSymbol"),
                "Transcript": transcript.get("transcriptId"),
                "CDS_Change": transcript.get("cdsChange"),
                "AA_Change": transcript.get("aminoAcidsChange"),
                "Effect": ";".join(transcript.get("calculatedEffects", [])),
                "Chr": var.get("chromosome"),
                "Pos": var.get("position"),
                "Ref": var.get("referenceAllele"),
                "Alt": var.get("alternateAllele"),
                "VAF": var.get("alternateAlleleFrequency"),
                "TotalDepth": var.get("totalReadDepth"),
                "AltDepth": var.get("alternateAlleleReadDepth"),
                "Cytoband": var.get("cytoband"),
                "ClinVar": ";".join(var.get("database", {}).get("clinVar", [])),
                "dbSNP": ";".join(var.get("database", {}).get("dbSNP", [])),
                "Validated": var.get("validated")
            })

    # Parse rearrangements
    rearrangements = json_data.get("variants", {}).get("rearrangements", [])
    for var in rearrangements:
        breakends = var.get("breakends", [])
        if len(breakends) >= 2:
            gene1 = breakends[0].get("transcripts", [{}])[0].get("geneSymbol", "-")
            gene2 = breakends[1].get("transcripts", [{}])[0].get("geneSymbol", "-")
            chr1 = breakends[0].get("chromosome")
            chr2 = breakends[1].get("chromosome")
            pos1 = breakends[0].get("startPosition")
            pos2 = breakends[1].get("startPosition")
            cytoband1 = breakends[0].get("cytoband")
            cytoband2 = breakends[1].get("cytoband")
        else:
            gene1, gene2 = "-", "-"
            chr1, chr2 = None, None
            pos1, pos2 = None, None
            cytoband1, cytoband2 = None, None

        rearrangement_records.append({
            "CaseID": case_data.get("caseId", ""),
            "ItemID": var.get("itemId"),
            "Gene": f"{gene1};{gene2}",
            "Chr": f"{chr1};{chr2}",
            "Pos": f"{pos1};{pos2}",
            "Cytoband": f"{cytoband1};{cytoband2}",
            "VAF": var.get("alternateAlleleFrequency"),
            "TotalReadCount": var.get("totalReadCount"),
            "SupportingReadCount": var.get("supportingReadCount"),
            "RearrangementType": var.get("rearrangementType"),
            "InsertedSequence": var.get("insertedSequence"),
            "Mitelman": ";".join(var.get("function", {}).get("mitelman", [])),
            "Validated": var.get("validated")
        })
    # Parse sequencing samples
    sequencing_samples = json_data.get("sequencingSamples", [])
    for sample in sequencing_samples:
        sequencing_saples.append({
            "CaseID": case_data.get("caseId", ""),
            "ItemID": sample.get("itemId"),
            "TumorOrNormal": sample.get("tumorOrNormal"),
            "NucleicAcid": sample.get("nucleicAcid"),
            "DuplicateReadsPercentage": sample.get("duplicateReadsPercentage"),
            "MeanReadDepth": sample.get("meanReadDepth"),
            "MappedReadsNumber": sample.get("mappedReadsNumber"),
            "Coverage100x": sample.get("coverage100x"),
            "QCStatus": sample.get("qcStatus"),
            "SpecimenIntactFfpe": sample.get("specimenIntactFfpe")
        })

    # Create DataFrames
    case_df = pd.DataFrame(case_info)
    short_df = pd.DataFrame(short_variant_records)
    rearrangement_df = pd.DataFrame(rearrangement_records)
    sequencing_df = pd.DataFrame(sequencing_saples)
    
    return case_df, short_df, rearrangement_df, sequencing_df


def detect_file_format(content: Union[str, bytes], filename: str) -> str:
    """Detect file format: FoundationOne XML, GenMineTOP XML, Guardant360 Excel, or HemeSight JSON"""
    if isinstance(content, str):
        # XML content
        if 'foundationmedicine.com' in content:
            return 'foundationone'
        elif 'todai-oncopanel' in content:
            return 'genminetop'
        else:
            return 'unknown'
    
    elif isinstance(content, bytes):
        # Binary content
        if filename.lower().endswith(('.xlsx', '.xls')):
            if 'Interim_' in filename and 'Guardant' in filename.upper() or filename.startswith('Interim_'):
                return 'guardant360'
            else:
                return 'excel_unknown'
        
        elif filename.lower().endswith('.json'):
            try:
                import json
                data = json.loads(content)
                if data.get("testInfo", {}).get("softwareName", "").startswith("ヘムサイト解析プログラム"):
                    return "hemesight"
                else:
                    return "json_unknown"
            except Exception:
                return "invalid_json"
    
    return "unknown"


def detect_xml_format(xml_content: str) -> str:
    """Detect whether XML is FoundationOne or GenMineTOP format"""
    if 'foundationmedicine.com' in xml_content:
        return 'foundationone'
    elif 'todai-oncopanel' in xml_content:
        return 'genminetop'
    else:
        return 'unknown'