class Base:
    NEME_SPACE = {
        'rr': 'http://integration.foundationmedicine.com/reporting',
        'vr': 'http://foundationmedicine.com/compbio/variant-report-external'
    }


class Abbreviation:
    ABBR_PATHOGENICITY = {
        'Pathogenic': 'P',
        'Pathogenic/Likely pathogenic': 'P/LP',
        'Pathogenic/Likely_pathogenic': 'P/LP',
        'Likely pathogenic': 'LP',
        'Likely_pathogenic': 'LP',
        'Uncertain significance': 'VUS',
        'Uncertain_significance': 'VUS',
        'Likely benign': 'LB',
        'Likely_benign': 'LB',
        'Benign/Likely benign': 'B/LB',
        'Benign/Likely_benign': 'B/LB',
        'Likely benign/Benign': 'LB/B',
        'Likely_benign/Benign': 'LB/B',
        'Benign': 'B',
        'Oncogenic': 'O',
        'Likely oncogenic': 'LO',
        'Likely_oncogenic': 'LO',
        'drug response': 'DR',
        'Conflicting classifications of pathogenicity': '§',
    }

    ABBR_STAR = {
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
    
    ABBR_DISEASE_NAME = {
        'Mixed-phenotype acute leukaemia': 'MPAL', 
        'Acute myeloid leukemia': 'AML', 
        'Acute lymphoblastic leukemia': 'ALL',
        'Chronic myeloid leukemia': 'CML', 
        'Chronic lymphocytic leukemia': 'CLL', 
        'Myelodysplastic syndrome': 'MDS',
        'Myeloproliferative neoplasm': 'MPN', 
        'Myelodysplastic/myeloproliferative neoplasm': 'MDS/MPN',
        'Myeloid neoplasm': 'MN', 
        'Lymphoid neoplasm': 'LN', 
        'Plasma cell neoplasm': 'PCN', 
        'Histocytic neoplasm': 'HN'
    }

    
class Transcript:
    TRANSCRIPT_ID = {
        'MYC': 'NM_002467.6', 
        'IGH': 'NM_001351.3', 
        'DUX4': 'NM_001306068.3', 
        'FGFR3': 'NM_001442.4',
        'GATA2': 'NM_032638.4', 
        'TRA': 'NM_001001912.3', 
        'CCND1': 'NM_053056.3',
        'MUTYH': 'NM_001128425.2',
        'MYD88': 'NM_002468.4',
    }

class Gene:
    HUGO_SYMBOL = {
        'MLL': 'KMT2A',
        'MLL2': 'KMT2D',
        'C17orf39': 'GID4',
        'PARK2': 'PRKN',
        'MRE11A': 'MRE11',
        'H3-3A': 'H3F3A'
    }

class Database:
    CIVIC_PATH = '../db/nightly-FeatureSummaries.tsv'
    COSMIC_PATH = 'Cosmic_CancerGeneCensus_v*_GRCh38.tsv'
    HGNC_PATH = '../db/protein-coding_gene.tsv'
    JSA_PATH = 'app/db/JSH_Guidelines.csv'
    LOGO_PATH = 'app/template/Logo.png'
    PGPV_PATH = '../db/pgpv.csv'
    TP53_PATH = '../db/MutationView_r21.csv'
    
    
class Hyperlink:
    CKB_LINK = 'https://ckb.genomenon.com/gene/show?geneId='
    CLINGEN_LINK = 'https://reg.clinicalgenome.org/redmine/projects/registry/genboree_registry/allele?hgvsOrDescriptor='
    CLINVAR_LINK = 'https://www.ncbi.nlm.nih.gov/clinvar/?term='
    CLINVAR_SEARCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    CLINVAR_SUMMARY = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    COSMIC_LINK = 'https://cancer.sanger.ac.uk/cosmic/search?q='
    DBSNP_LINK = 'https://www.ncbi.nlm.nih.gov/snp/?term='
    FRANKLIN_LINK = 'https://franklin.genoox.com/clinical-db/variant/snp'
    GENEBE_LINK = 'https://genebe.net/variant/'
    GNOMAD_LINK = 'https://gnomad.broadinstitute.org/variant'
    JCGA_LINK = 'https://www.jcga-scc.jp/ja/gene/'
    JMORP_LINK = 'https://jmorp.megabank.tohoku.ac.jp/search?query='
    MASTERMIND_LINK = 'https://mastermind.genomenon.com/detail?mutation='
    OMIM_LINK = 'https://www.ncbi.nlm.nih.gov/omim/?term='
    ONCOKB_LINK = 'https://www.oncokb.org/gene/'
    TOGOVAR_38_LINK = 'https://grch38.togovar.org/?mode=simple&term='
    TOGOVAR_37_LINK = 'https://grch37.togovar.org/?mode=simple&term='
    STJUDE_LINK = 'https://pecan.stjude.cloud/variants/proteinpaint?gene='
    VARSOME_38_LINK = 'https://www.varsome.com/variant/hg38/'
    VARSOME_19_LINK = 'https://www.varsome.com/variant/hg19/'
    

class Columns:
    SNV_INDEL = ['geneSymbol', 'aminoAcidsChange', 'alternateAlleleFrequency', 'Role_in_Cancer', 'GeneBe_TOMMO_dbSNP', 
        'GeneBe_ClinVar_Germline', 'GeneBe_ClinVar_Somatic', 'GeneBe_ACMG_classification', 'status']
    
    FOUNDATION_CNV = ['geneSymbol', 'Role_in_Cancer', 'copyNumber', 'numberOfExons', 'type', 'equivocal', 'status']
    FOUNDATION_FUSION = ['description', 'inFrame', 'type', 'equivocal', 'status']
    FOUNDATION_GERMLINE = ['geneSymbol', 'aminoAcidsChange', 'cdsChange', 'alternateAlleleFrequency']

    GENMINE_CNV = ['geneSymbol', 'Role_in_Cancer', 'copyNumber', 'type', 'status']
    GENMINE_FUSION = ['Fusion_Gene', 'Breakpoint', 'type', 'frame', 'status']
    
    GUARDANT_CNV = ['geneSymbol', 'Role_in_Cancer', 'copyNumber', 'chromosome', 'type', 'status']
    
    HEMESIGHT_SHORT = ['itemId', 'geneSymbol', 'aminoAcidsChange', 'alternateAlleleFrequency', 'Role_in_Cancer', 
                       'database.tommo', 'database.gnomAD', 'GeneBe_ClinVar_Germline', 'database.cosmicHeme']
    HEMESIGHT_REARRANGEMENT = ['itemId', 'geneSymbol', 'number.number', 'rearrangementType', 'insertedSequence', 
                               'function.mitelman', 'chromosome', 'startPosition']
    HEMESIGHT_SV = ['geneSymbol_0', 'geneSymbol_1', 'rearrangementType_0', 'insertedSequence_0', 'function.mitelman_0']
    HEMESIGHT_FU = ['geneSymbol_0', 'geneSymbol_1', 'rearrangementType_0', 'function.mitelman_0']
    HEMESIGHT_JSA = ['Gene', 'Disease', 'PathogenicVariants', 'EV_Diagnosis', 'EV_Treatment', 'EV_Prognosis']
    HEMESIGHT_FASTTRACK_SNV = ["Gene_FastTrack", "Protein_FastTrack", "Gene", "Protein", "Mutation_Type", "Mutation_Allele_Frequency"]
    HEMESIGHT_FASTTRACK_CNV = ["Gene_FastTrack", "Protein_FastTrack", "Gene_1", "Cytoband_1", "Gene_2", "Cytoband_2", "Mutation_Type"]
    
    PROTEINPAINT = ['itemId', 'chr_a', 'chr_b', 'gene_a', 'gene_b', 'position_a', 'position_b']
    DISCO = ['chr_a', 'position_a', 'gene_a', 'chr_b', 'position_b', 'gene_b']
    
    DEFAULT = ['GeneBe_variant', 'GeneBe_geneID', 'GeneBe_dbSNP', 'GeneBe_effect',
                   'GeneBe_ACMG_score', 'GeneBe_ACMG_classification', 'GeneBe_ACMG_criteria',
                   'GeneBe_ClinVar_Germline', 'GeneBe_ClinVar_Germline_Status',
                   'GeneBe_ClinVar_Somatic', 'GeneBe_ClinVar_Somatic_Status',
                   'GeneBe_ClinVar_Classification', 'GeneBe_ClinVar_Submission_Summary',
                   'GeneBe_AlphaMissense_Score', 'GeneBe_AlphaMissense_Prediction',
                   'GeneBe_gnomAD_Exomes_AF', 'GeneBe_gnomAD_Genomes_AF', 'GeneBe_TOMMO_dbSNP']
    

class ReadRange:
    FASTTRACK = [
        {
            "name": "Disease",
            "start_marker": "検査依頼時の情報",
            "end_marker": "疾患分類 （自動選択）",
            "columns": ["Gene_FastTrack", "Protein_FastTrack", "ID", "Gene", "Protein", "Mutation_Type", "Mutation_Allele_Frequency"]
        },
        {
            "name": "SNV_Indel",
            "start_marker": "ID 遺伝子名 アミノ酸変化 変異種別 変異アレル頻度",
            "end_marker": "構造異常",
            "columns": ["Gene_FastTrack", "Protein_FastTrack", "ID", "Gene", "Protein", "Mutation_Type", "Mutation_Allele_Frequency"]
        },
        {
            "name": "SV",
            "start_marker": "遺伝子名 サイトバンド 遺伝子名 サイトバンド",
            "end_marker": "注意事項",
            "columns": ["Gene_FastTrack", "Protein_FastTrack", "ID", "Gene_1", "Cytoband_1", "Gene_2", "Cytoband_2", "Mutation_Type"]
        }
    ]
    