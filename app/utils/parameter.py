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
        "Aplastic anemia": "AA",
        "Atypical chronic myeloid leukaemia, BCR-ABL1-negative": "aCML",
        "Acute erythroid leukaemia": "AEL",
        "Angioimmunoblastic T-cell lymphoma": "AITL",
        "Anaplastic large cell lymphoma": "ALCL",
        "anaplastic large cell lymphoma, ALK-positive": "ALCL (ALK+)",
        "Acute lymphoblastic leukaemia/lymphoma": "ALL",
        "Autoimmune lymphoproliferative syndrome": "ALPS",
        "Acute megakaryoblastic leukaemia": "AMKL",
        "Acute myeloid leukaemia": "AML",
        "Acute myeloid leukaemia with myelodysplasia-related changes": "AML with MRC",
        "Aggressive NK-cell leukaemia": "ANKL",
        "Activated PI3Kδ syndrome": "APDS",
        "Acute promyelocytic leukaemia with PML-RARA": "APL",
        "Adult T-cell leukaemia/lymphoma": "ATLL",
        "Acute undifferentiated leukaemia": "AUL",
        "B- lymphoblastic leukaemia/lymphoma": "B-ALL/LBL",
        "Burkitt lymphoma": "BL",
        "Burkitt lymphoma with 11q aberration": "BL11q",
        "Blastic plasmacytoid dendritic cell neoplasm": "BPDCN",
        "Primary cutaneous anaplastic large cell lymphoma": "C-ALCL",
        "Clonal hematopoiesis of indeterminate potential": "CHIP",
        "Classical Hodgkin lymphoma": "CHL",
        "Chronic lymphocytic leukaemia": "CLL",
        "Chronic lymphocytic leukaemia/ small lymphocytic lymphoma": "CLL/SLL",
        "Chronic lymphoproliferative disorder of NK cells": "CLPD-NK",
        "Chronic myeloid leukaemia, BCR-ABL1-positive": "CML",
        "Chronic myelomonocytic leukaemia": "CMML",
        "Chronic neutrophilic leukaemia": "CNL",
        "Diffuse large B-cell lymphoma, not otherwise specified": "DLBCL",
        "Enteropathy-associated T-cell lymphoma": "EATL",
        "Duodenal-type follicular lymphoma": "DFL",
        "Extranodal marginal zone lymphoma": "EMZL",
        "Extranodal NK/T cell lymphoma, nasal type": "ENKTL",
        "Essential thrombocythemia": "ET",
        "Early T-cell precursor ALL": "ETP-ALL",
        "Follicular dendritic cell sarcoma": "FDCS",
        "Follicular lymphoma": "FL",
        "Follicular T-cell lymphoma": "FTCL",
        "Hairy cell leukaemia": "HCL",
        "Hairy cell leukaemia variant": "HCL-v",
        "Histiocytic and dendritic cell neoplasms": "HCDN",
        "High-grade B-cell lymphoma": "HGBL",
        "Hemophagocytic lymphohistiocytosis": "HLH",
        "Hepatosplenic T-cell lymphoma": "HSTL",
        "Intrachromosomal amplification of chromosome 21-ALL": "iAMP21-ALL",
        "Inherited bone marrow failure syndromes": "IBMFS",
        "Interdigitating dendritic cell sarcoma": "IDCS",
        "Indolent NK-cell lymphoproliferative disorder of the gastrointestinal tract": "iNKLPD",
        "Intestinal T cell lymphoma, NOS": "ITCL-NOS",
        "Juvenile myelomonocytic leukaemia": "JMML",
        "ALK-positive large B-cell lymphoma": "LBCL (ALK+)",
        "Large B-cell lymphoma with IRF4 rearrangement": "LBCL with IRF4-r",
        "Lymphoplasmacytic lymphoma": "LPL",
        "Extranodal marginal zone lymphoma of mucosa-associated lymphoid tissue": "MALT",
        "Monoclonal B lymphocytosis": "MBL",
        "Mantle cell lymphoma": "MCL",
        "Myelodysplastic syndromes": "MDS",
        "Myelodysplastic/myeloproliferative neoplasm with ring sideroblasts and thrombocytosis": "MDS/MPN-RS-T",
        "Monomorphic epitheliotropic intestinal T-cell lymphoma": "MEITL",
        "Myeloid/lymphoid neoplasms with eosinophilia": "MLN-e",
        "Multiple myeloma": "MM",
        "Mixed-phenotype acute leukaemia": "MPAL",
        "Mature plasmacytoid dendritic cells proliferation associated with myeloid neoplasms": "MPDMN",
        "Myeloproliferative neoplasms": "MPN",
        "Monomorphic post-transplant lymphoproliferative disorder": "M-PTLD",
        "Nodal peripehral T-cell lymphoma with T follicular helper phenotype": "Nodal PTCL with TFH phenotype",
        "Non-Hodgkin lymphoma": "NHL",
        "NK-large granular lymphocytic leukaemia": "NKLGLL",
        "Nodular lymphocyte predominant Hodgkin lymphoma": "NLPHL",
        "Nodal marginal zone lymphoma": "NMZL",
        "Plasmablastic lymphoma": "PBL",
        "Primary cutaneous CD8+ aggressive epidermotropic cytotoxic T-cell lymphoma": "PCAETCL",
        "Primary cutaneous follicle center lymphoma": "PCFCL",
        "Primary cutaneous marginal zone lymphoma": "PCMZL",
        "Primary diffuse large B-cell lymphoma of the central nervous system (CNS)": "PCNSL",
        "Primary mediastinal large B-cell lymphoma": "PMBL",
        "Primary myelofibrosis": "PMF",
        "Paroxysmal nocturnal hemoglobinuria": "PNH",
        "Peripheral T-cell lymphoma, not otherwise specified": "PTCL-NOS",
        "Pediatric-type follicular lymphoma": "PTFL",
        "Post-transplant lymphoproliferative disorders": "PTLD",
        "Polymorphic post-transplant lymphoproliferative disorders": "P-PTLD",
        "Polycythemia vera": "PV",
        "Splenic B-cell lymphoma/leukaemia with prominent nucleoli": "SBLPN",
        "Splenic diffuse red pulp small B-cell lymphoma": "SDRPL",
        "Systemic mastocytosis": "SM",
        "Systemic mastocytosys with an associated hematological neoplasm": "SM-AHN",
        "Splenic marginal zone lymphoma": "SMZL",
        "Sézary syndrome": "SS",
        "Subcutaneous panniculitis-like T-cell lymphoma": "SPTCL",
        "Transient abnormal myelopoiesis": "TAM",
        "T-lymphoblastic leukaemia/lymphoma": "T-ALL",
        "T-cell large granular lymphocytic leukaemia": "T-LGL",
        "Therapy-related myeloid neoplasms": "t-MNs",
        "T-cell Non-Hodgkin lymphoma": "T-NHL",
        "T-cell prolymphocytic leukaemia": "T-PLL",
        "Transient abnormal myelopoiesis associated with Down syndrome": "TAM",
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
    