import os

import pandas as pd

from .web_scraping import fetch_genebe, fetch_tommo, fetch_clinvar
from .parameter import Abbreviation, Database, Hyperlink

def link_generator(analysis_type, row, gene_id, transcript_id, chromosome, pos, ref, alt,
                   cds_change, gene_symbol, amino_acids_change, dbsnp):

    # GeneBe データ取得
    genebe_json, variant, chromosome, position, ref, alt, dbsnp = fetch_genebe(analysis_type, transcript_id, cds_change)
    variant_data = genebe_json[0] if genebe_json else {}

    consequences = variant_data.get('consequences', [])
    first_consequence = consequences[0] if consequences else {}

    clinvar_data = fetch_clinvar(transcript_id, gene_symbol, cds_change, dbsnp)
    germline_sig = clinvar_data[0] if len(clinvar_data) > 0 else None
    germline_review = clinvar_data[1] if len(clinvar_data) > 1 else None
    somatic_sig = clinvar_data[2] if len(clinvar_data) > 2 else None
    somatic_review = clinvar_data[3] if len(clinvar_data) > 3 else None
    
    acmg_classification = variant_data.get('acmg_classification')
    clin_sig = variant_data.get('clinvar_classification')
    
    sig_mapping = Abbreviation.ABBR_PATHOGENICITY
    germline_sig = sig_mapping.get(germline_sig, germline_sig) if germline_sig else None
    somatic_sig = sig_mapping.get(somatic_sig, somatic_sig) if somatic_sig else None
    acmg_classification = sig_mapping.get(acmg_classification, acmg_classification) if acmg_classification else None
    clin_sig = sig_mapping.get(clin_sig, clin_sig) if clin_sig else None
    
    review_mapping = Abbreviation.ABBR_STAR
    germline_status = review_mapping.get(germline_review, germline_review) if germline_review else None
    somatic_status = review_mapping.get(somatic_review, somatic_review) if somatic_review else None

    # GeneBe データの格納
    genebe_dic = {
            'GeneBe_variant': variant,
            'GeneBe_geneID': gene_id,
            'GeneBe_dbSNP': dbsnp,
            'GeneBe_effect': first_consequence.get('consequences', [None])[0] if first_consequence else None,
            'GeneBe_ACMG_score': variant_data.get('acmg_score'),
            'GeneBe_ACMG_classification': acmg_classification,
            'GeneBe_ACMG_criteria': variant_data.get('acmg_criteria'),
            'GeneBe_ClinVar_Germline': germline_sig,
            'GeneBe_ClinVar_Germline_Status': germline_status,
            'GeneBe_ClinVar_Somatic': somatic_sig,
            'GeneBe_ClinVar_Somatic_Status': somatic_status,
            'GeneBe_ClinVar_Classification': clin_sig,
            'GeneBe_ClinVar_Submission_Summary': variant_data.get('clinvar_submissions_summary'),
            'GeneBe_AlphaMissense_Score': variant_data.get('alphamissense_score'),
            'GeneBe_AlphaMissense_Prediction': variant_data.get('alphamissense_prediction'),
            'GeneBe_gnomAD_Exomes_AF': f"{variant_data.get('gnomad_exomes_af', 0):.3e}" if variant_data.get('gnomad_exomes_af') is not None else "N/A",
            'GeneBe_gnomAD_Genomes_AF': f"{variant_data.get('gnomad_genomes_af', 0):.3e}" if variant_data.get('gnomad_genomes_af') is not None else "N/A",
            'GeneBe_TOMMO_dbSNP': fetch_tommo(transcript_id, cds_change, alt, dbsnp)
        }
    if analysis_type != 'Guardant360':
        row.update(genebe_dic)
    else:
        row = genebe_dic        
        
    # CiVIC処理
    base_path = os.path.dirname(__file__)
    civic_file_path = os.path.join(base_path, Database.CIVIC_PATH)
    civic_df = pd.read_csv(civic_file_path, sep='\t', encoding='utf-8', low_memory=False)
    match = civic_df[civic_df['name'] == gene_symbol]
    if not match.empty:
        row['CiVIC'] = f'=HYPERLINK("{match.iloc[0]["feature_civic_url"]}", "CiVIC")'
    else:
        row['CiVIC'] = '-'
    
    hgnc_file_path = os.path.join(base_path, Database.HGNC_PATH)
    civic_df = pd.read_csv(hgnc_file_path, sep='\t', encoding='utf-8', low_memory=False)
    civic_gene = civic_df[civic_df['symbol'] == gene_symbol]
    if not civic_gene.empty:
        gene_id = str(civic_gene['entrez_id'].values[0])
            
    row['CKB CORE'] = f'=HYPERLINK("{Hyperlink.CKB_LINK}{gene_id}", "CKB CORE")'
    row['ClinGen'] = f'=HYPERLINK("{Hyperlink.CLINGEN_LINK}{transcript_id}:{cds_change}", "ClinGen")'
    row['ClinVar'] = f'=HYPERLINK("{Hyperlink.CLINVAR_LINK}{transcript_id}:{cds_change}", "ClinVar")'   
    row['COSMIC'] = f'=HYPERLINK("{Hyperlink.COSMIC_LINK}{gene_symbol}+{cds_change}", "COSMIC")'
    row['GeneBe'] = f'=HYPERLINK("{Hyperlink.GENEBE_LINK}hg38/{transcript_id}:{cds_change}", "GeneBe")'
    
    MAX_URL_LENGTH = 128
    url = f"{chromosome}-{pos}-{ref}-{alt}"
    if analysis_type in ['GenMineTOP', 'HemeSight']:
        row['TogoVar'] = f'=HYPERLINK("{Hyperlink.TOGOVAR_38_LINK}{chromosome}%3A{pos}", "TogoVar")'
        row['Varsome'] = f'=HYPERLINK("{Hyperlink.VARSOME_38_LINK}{transcript_id}:{cds_change}", "Varsome")'
        if len(url) <= MAX_URL_LENGTH:
            row['Franklin'] = f'=HYPERLINK("{Hyperlink.FRANKLIN_LINK}/{chromosome}-{pos}-{ref}-{alt}-hg38", "Franklin")'
            row['gnomAD'] = f'=HYPERLINK("{Hyperlink.GNOMAD_LINK}/{chromosome}-{pos}-{ref}-{alt}?dataset=gnomad_r4", "gnomAD")'
        else:
            row['Franklin'] = "URL too long"
            row['gnomAD'] = "URL too long"
    else:
        row['TogoVar'] = f'=HYPERLINK("{Hyperlink.TOGOVAR_37_LINK}{chromosome}%3A{pos}", "TogoVar")'
        row['Varsome'] = f'=HYPERLINK("{Hyperlink.VARSOME_19_LINK}{transcript_id}:{cds_change}", "Varsome")'
        if len(url) <= MAX_URL_LENGTH:
            row['Franklin'] = f'=HYPERLINK("{Hyperlink.FRANKLIN_LINK}/{chromosome}-{pos}-{ref}-{alt}-hg19", "Franklin")'
            row['gnomAD'] = f'=HYPERLINK("{Hyperlink.GNOMAD_LINK}/{chromosome}-{pos}-{ref}-{alt}?dataset=gnomad_r2_1", "gnomAD")'
        else:
            row['Franklin'] = "URL too long"
            row['gnomAD'] = "URL too long"

    row['JCGA'] = f'=HYPERLINK("{Hyperlink.JCGA_LINK}{gene_symbol}", "JCGA")'
    if gene_symbol and amino_acids_change:
        aa_change = amino_acids_change[2:] if amino_acids_change.startswith('p.') else amino_acids_change
        row['jMorp'] = f'=HYPERLINK("{Hyperlink.JMORP_LINK}{gene_symbol}+{aa_change}", "jMorp")'
    row['Mastermind'] = f'=HYPERLINK("{Hyperlink.MASTERMIND_LINK}{gene_symbol}:{cds_change}", "Mastermind")'
    row['OMIM'] = f'=HYPERLINK("{Hyperlink.OMIM_LINK}{gene_symbol}", "OMIM")'
    row['OncoKB'] = f'=HYPERLINK("{Hyperlink.ONCOKB_LINK}{gene_symbol}", "OncoKB")'
    row['St.Jude'] = f'=HYPERLINK("{Hyperlink.STJUDE_LINK}{gene_symbol}", "St.Jude")'
    
    # TP53処理
    tp53_file_path = os.path.join(base_path, Database.TP53_PATH)
    if gene_symbol == 'TP53':
        tp53_df = pd.read_csv(tp53_file_path, sep=',', encoding='utf-8')
        tp53_df['TP53_h19'] = tp53_df['g_description'].str.replace('g.', '', regex=False)
        tp53_dict = {row_data['TP53_h19']: row_data['TransactivationClass'] for _, row_data in tp53_df.iterrows() if pd.notna(row_data['TP53_h19'])}
        
        tp53_key = f"{pos}{ref}>{alt}"
        row['TP53'] = tp53_dict.get(tp53_key, 'NA')

    else:
        row['TP53'] = '-' if gene_symbol != 'TP53' else 'NA'

    return row