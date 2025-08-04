import streamlit as st
import genebe as gnb
from annotator.link_generator import generate_links
from annotator.data_fetch import fetch_tommo_data, fetch_clinvar_data, fetch_tp53_data, fetch_role_tier, fetch_cosmic_data

def process_variant(grc, variant):
    """Parse and annotate a variant, returning results"""
    try:
        if grc == 'hg38':
            grc_b = 'hg19'
            hg38 = gnb.parse_variants([f"{variant}"], genome=grc)[0]
            chromosome, position, ref, alt = hg38.split('-')
            hg19 = gnb.lift_over_variants([hg38], from_genome=grc, dest_genome=grc_b)[0]
            position_hg19 = hg19.split('-')[1]
            
            
        elif grc == 'hg19':
            grc_b = 'hg38'
            hg38 = gnb.lift_over_variants([variant], from_genome=grc, dest_genome=grc_b)[0]
            chromosome, position, ref, alt = hg38.split('-')
            position_hg19 = variant.split('-')[1]

        genebe_json = gnb.annotate_variants_list([f"{hg38}"], flatten_consequences=False, genome="hg38")

        if not genebe_json:
            return None

        gene_symbol = genebe_json[0].get('gene_symbol')
        hgvs_c = genebe_json[0]['consequences'][0].get('hgvs_c')
        dbsnp = genebe_json[0].get('dbsnp')
        matching_consequences = [
            c for c in genebe_json[0]['consequences']
            if (hgvs_c and hgvs_c in (c.get('hgvs_c') or ''))
        ]

        if hgvs_c:
            consequence = matching_consequences[0] if matching_consequences else {}
            transcript_id = consequence.get('transcript')
            hgvs_p = consequence.get('hgvs_p')
            effect = consequence.get('consequences', [None])[0]
        else:
            transcript_id = genebe_json[0].get('transcript')
            hgvs_p = genebe_json[0]['consequences'][0].get('hgvs_p')
            effect = genebe_json[0]['consequences'][0].get('consequences', [None])[0]

        clinvar_data = fetch_clinvar_data(transcript_id, hgvs_c, dbsnp)
        germline_review = clinvar_data[1]
        somatic_review = clinvar_data[3]
        review_mapping = {
            'practice guideline': '★4',
            'reviewed by expert panel': '★3',
            'criteria provided, multiple submitters': '★2',
            'criteria provided, multiple submitters, no conflicts': '★2',
            'criteria provided, conflicting classifications': '★1',
            'criteria provided, single submitter': '★1',
            'no assertion criteria provided': '★0',
            'no classification provided': '★0',
            'no classification for the individual variant': '★0'
        }
        germline_status = review_mapping.get(germline_review, germline_review)
        somatic_status = review_mapping.get(somatic_review, somatic_review)

        data = {
            'Variant_input': variant,
            'Chromosome': chromosome,
            'hg38 Position': position,
            'hg19 Position': position_hg19,
            'Reference Allele': ref,
            'Alternate Allele': alt,
            'Gene Symbol': gene_symbol,
            'Transcript ID': transcript_id,
            'HGVS cDNA': hgvs_c,
            'HGVS Protein': hgvs_p,
            'dbSNP ID': genebe_json[0].get('dbsnp'),
            'Effect': effect,
            'ACMG Score': genebe_json[0].get('acmg_score'),
            'ACMG Classification': genebe_json[0].get('acmg_classification'),
            'ACMG Criteria': genebe_json[0].get('acmg_criteria'),
            'ClinVar ID': fetch_clinvar_data(transcript_id, hgvs_c, dbsnp)[4],
            'ClinVar Germline': fetch_clinvar_data(transcript_id, hgvs_c, dbsnp)[0],
            'ClinVar Germline Status': germline_status,
            'ClinVar Somatic': fetch_clinvar_data(transcript_id, hgvs_c, dbsnp)[2],
            'ClinVar Somatic Status': somatic_status,
            'ClinVar Classification_GeneBe': genebe_json[0].get('clinvar_classification'),
            'ClinVar Submission Summary_GeneBe': genebe_json[0].get('clinvar_submissions_summary'),
            'AlphaMissense Score': genebe_json[0].get('alphamissense_score'),
            'AlphaMissense Prediction': genebe_json[0].get('alphamissense_prediction'),
            'gnomAD Exomes AF': f"{genebe_json[0].get('gnomad_exomes_af', 0):.3e}" if genebe_json[0].get('gnomad_exomes_af') is not None else "N/A",
            'gnomAD Genomes AF': f"{genebe_json[0].get('gnomad_genomes_af', 0):.3e}" if genebe_json[0].get('gnomad_genomes_af') is not None else "N/A",
            'TOMMO_dbSNP': fetch_tommo_data(transcript_id, hgvs_p, alt, genebe_json[0].get('dbsnp')),
            'TP53': fetch_tp53_data(position, ref, alt, gene_symbol),
            **{k: v for k, v in zip(
                ['Role in Cancer_CancerGeneCensus', 'Tier_CancerGeneCensus', 'Tumor Type Somatic_CancerGeneCensus', 'Tumor Type Germline_CancerGeneCensus', 'Cancer Syndrome_CancerGeneCensus'],
                fetch_role_tier(gene_symbol)
            )},
            **{k: v for k, v in zip(
                ['COSMIC Sample Tested', 'COSMIC Sample Mutated'],
                fetch_cosmic_data(gene_symbol, hgvs_c, hgvs_p)
            )},
            **generate_links(chromosome, position, ref, alt, transcript_id, gene_symbol, hgvs_c, hgvs_p)
        }
        return data
    except Exception as e:
        st.warning(f"{variant} 解析エラー: {e}")
        return None