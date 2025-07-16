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
        "aplastic anemia": "AA",
        "atypical chronic myeloid leukemia, BCR-ABL1-negative": "aCML",
        "acute erythroid leukemia": "AEL",
        "angioimmunoblastic T-cell lymphoma": "AITL",
        "anaplastic large cell lymphoma": "ALCL",
        "anaplastic large cell lymphoma, ALK-positive": "ALCL (ALK+)",
        "acute lymphoblastic leukemia/lymphoma": "ALL",
        "autoimmune lymphoproliferative syndrome": "ALPS",
        "acute megakaryoblastic leukemia": "AMKL",
        "acute myeloid leukemia": "AML",
        "acute myeloid leukemia with myelodysplasia-related changes": "AML with MRC",
        "aggressive NK-cell leukemia": "ANKL",
        "activated PI3Kδ syndrome": "APDS",
        "acute promyelocytic leukemia with PML-RARA": "APL",
        "adult T-cell leukemia/lymphoma": "ATLL",
        "acute undifferentiated leukemia": "AUL",
        "B- lymphoblastic leukemia/lymphoma": "B-ALL/LBL",
        "Burkitt lymphoma": "BL",
        "Burkitt lymphoma with 11q aberration": "BL11q",
        "blastic plasmacytoid dendritic cell neoplasm": "BPDCN",
        "primary cutaneous anaplastic large cell lymphoma": "C-ALCL",
        "clonal hematopoiesis of indeterminate potential": "CHIP",
        "classical Hodgkin lymphoma": "CHL",
        "chronic lymphocytic leukemia": "CLL",
        "chronic lymphocytic leukemia/ small lymphocytic lymphoma": "CLL/SLL",
        "chronic lymphoproliferative disorder of NK cells": "CLPD-NK",
        "chronic myeloid leukemia, BCR-ABL1-positive": "CML",
        "chronic myelomonocytic leukemia": "CMML",
        "chronic neutrophilic leukemia": "CNL",
        "diffuse large B-cell lymphoma, not otherwise specified": "DLBCL",
        "enteropathy-associated T-cell lymphoma": "EATL",
        "duodenal-type follicular lymphoma": "DFL",
        "extranodal marginal zone lymphoma": "EMZL",
        "extranodal NK/T cell lymphoma, nasal type": "ENKTL",
        "essential thrombocythemia": "ET",
        "early T-cell precursor ALL": "ETP-ALL",
        "follicular dendritic cell sarcoma": "FDCS",
        "follicular lymphoma": "FL",
        "follicular T-cell lymphoma": "FTCL",
        "hairy cell leukemia": "HCL",
        "hairy cell leukemia variant": "HCL-v",
        "histiocytic and dendritic cell neoplasms": "HCDN",
        "high-grade B-cell lymphoma": "HGBL",
        "hemophagocytic lymphohistiocytosis": "HLH",
        "hepatosplenic T-cell lymphoma": "HSTL",
        "intrachromosomal amplification of chromosome 21-ALL": "iAMP21-ALL",
        "inherited bone marrow failure syndromes": "IBMFS",
        "interdigitating dendritic cell sarcoma": "IDCS",
        "indolent NK-cell lymphoproliferative disorder of the gastrointestinal tract": "iNKLPD",
        "intestinal T cell lymphoma, NOS": "ITCL-NOS",
        "juvenile myelomonocytic leukemia": "JMML",
        "ALK-positive large B-cell lymphoma": "LBCL (ALK+)",
        "large B-cell lymphoma with IRF4 rearrangement": "LBCL with IRF4-r",
        "lymphoplasmacytic lymphoma": "LPL",
        "extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue": "MALT",
        "monoclonal B lymphocytosis": "MBL",
        "mantle cell lymphoma": "MCL",
        "myelodysplastic syndromes": "MDS",
        "myelodysplastic/myeloproliferative neoplasm with ring sideroblasts and thrombocytosis": "MDS/MPN-RS-T",
        "monomorphic epitheliotropic intestinal T-cell lymphoma": "MEITL",
        "myeloid/lymphoid neoplasms with eosinophilia": "MLN-e",
        "multiple myeloma": "MM",
        "mixed-phenotype acute leukemia": "MPAL",
        "mature plasmacytoid dendritic cells proliferation associated with myeloid neoplasms": "MPDMN",
        "myeloproliferative neoplasms": "MPN",
        "monomorphic post-transplant lymphoproliferative disorder": "M-PTLD",
        "nodal peripehral T-cell lymphoma with T follicular helper phenotype": "Nodal PTCL with TFH phenotype",
        "Non-Hodgkin lymphoma": "NHL",
        "NK-large granular lymphocytic leukemia": "NKLGLL",
        "nodular lymphocyte predominant Hodgkin lymphoma": "NLPHL",
        "nodal marginal zone lymphoma": "NMZL",
        "plasmablastic lymphoma": "PBL",
        "primary cutaneous CD8+ aggressive epidermotropic cytotoxic T-cell lymphoma": "PCAETCL",
        "primary cutaneous follicle center lymphoma": "PCFCL",
        "primary cutaneous marginal zone lymphoma": "PCMZL",
        "primary diffuse large B-cell lymphoma of the central nervous system (CNS)": "PCNSL",
        "primary mediastinal large B-cell lymphoma": "PMBL",
        "primary myelofibrosis": "PMF",
        "paroxysmal nocturnal hemoglobinuria": "PNH",
        "peripheral T-cell lymphoma, not otherwise specified": "PTCL-NOS",
        "pediatric-type follicular lymphoma": "PTFL",
        "post-transplant lymphoproliferative disorders": "PTLD",
        "polymorphic post-transplant lymphoproliferative disorders": "P-PTLD",
        "polycythemia vera": "PV",
        "splenic B-cell lymphoma/leukemia with prominent nucleoli": "SBLPN",
        "splenic diffuse red pulp small B-cell lymphoma": "SDRPL",
        "systemic mastocytosis": "SM",
        "systemic mastocytosys with an associated hematological neoplasm": "SM-AHN",
        "splenic marginal zone lymphoma": "SMZL",
        "Sézary syndrome": "SS",
        "Subcutaneous panniculitis-like T-cell lymphoma": "SPTCL",
        "transient abnormal myelopoiesis": "TAM",
        "T-lymphoblastic leukemia/lymphoma": "T-ALL",
        "T-cell large granular lymphocytic leukemia": "T-LGL",
        "therapy-related myeloid neoplasms": "t-MNs",
        "T-cell Non-Hodgkin lymphoma": "T-NHL",
        "T-cell prolymphocytic leukemia": "T-PLL",
        "transient abnormal myelopoiesis associated with Down syndrome": "TAM",
        "T-cell/histiocyte-rich large B-cell lymphoma": "THRLBCL",
        "Waldenström macroglobulinemia": "WM",
        "X-linked lymphoproliferative disease": "XLP"
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

import os

class Database:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    CIVIC_PATH = os.path.join(BASE_DIR, 'app', 'db', 'nightly-FeatureSummaries.tsv')
    COSMIC_PATH = os.path.join(BASE_DIR, 'app', 'db', 'Cosmic_CancerGeneCensus_v*_GRCh38.tsv')
    COSMIC_37_PATH = os.path.join(BASE_DIR, 'app', 'db', 'CancerMutationCensus_Slim_v*_GRCh37.tsv.gz')
    HGNC_PATH = os.path.join(BASE_DIR, 'app', 'db', 'protein-coding_gene.tsv')
    JSA_PATH = os.path.join(BASE_DIR, 'app', 'db', 'JSH_Guidelines.csv')
    LOGO_PATH = os.path.join(BASE_DIR, 'app', 'template', 'Logo.png')
    PGPV_PATH = os.path.join(BASE_DIR, 'app', 'db', 'pgpv.csv')
    TP53_PATH = os.path.join(BASE_DIR, 'app', 'db', 'MutationView_r21.csv')

    
    
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
                               'function.mitelman', 'chromosome', 'startPosition', 'matePieceLocation', 'supportingReadCount']
    HEMESIGHT_SV = ['geneSymbol_0', 'geneSymbol_1', 'rearrangementType_0', 'insertedSequence_0', 'function.mitelman_0']
    HEMESIGHT_FU = ['geneSymbol_0', 'geneSymbol_1', 'rearrangementType_0', 'supportingReadCount_0', 'function.mitelman_0']
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
    
