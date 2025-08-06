# parameter.py

import glob


class DBPaths:
    """ローカルDBファイルのパス（バージョンに依存しないワイルドカード対応）"""
    TP53_CSV = "./app/db/MutationView_r21.csv"

    @staticmethod
    def get_cgc_tsv():
        """Cancer Gene Census のTSVファイルを取得（例: Cosmic_CancerGeneCensus_v101_GRCh38.tsv）"""
        candidates = glob.glob("./app/db/Cosmic_CancerGeneCensus_v*_GRCh38.tsv")
        return sorted(candidates)[-1] if candidates else None

    @staticmethod
    def get_cosmic_tsv_gz():
        """COSMICのTSV GZIPファイルを取得（例: cosmic_v94_hg19.tsv.gz）"""
        candidates = glob.glob("./app/db/CancerMutationCensus_AllData_v*_GRCh37_va.tsv.gz")
        return sorted(candidates)[-1] if candidates else None

    @staticmethod
    def get_civic_tsv():
        candidates = glob.glob("./app/db/nightly-FeatureSummaries.tsv")
        return candidates[0] if candidates else None

class URLs:
    """外部APIやウェブページのURLテンプレート"""
    NCBI_SNP = "https://www.ncbi.nlm.nih.gov/snp/?term={query}"
    CLINVAR_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    CLINVAR_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    LINK_TEMPLATES = {
        "VarSome":      "https://varsome.com/variant/hg38/{transcript_id}%20{hgvs_c}",
        "ClinVar":      "https://www.ncbi.nlm.nih.gov/clinvar/?term={transcript_id}({gene_symbol}):{hgvs_c}",
        "ClinGen":      "https://erepo.clinicalgenome.org/evrepo/ui/summary/classifications?columns=gene,preferredVarTitle&values={gene_symbol},{hgvs_c}&matchTypes=contains,contains&pgSize=25&pg=1&matchMode=and",
        "GeneBe":       "https://genebe.net/variant/hg38/{transcript_id}%20{hgvs_c}",
        "Franklin":     "https://franklin.genoox.com/clinical-db/variant/snp/{chromosome}-{position}-{ref}-{alt}-hg38",
        "gnomAD":       "https://gnomad.broadinstitute.org/variant/{chromosome}-{position}-{ref}-{alt}?dataset=gnomad_r4",
        "TogoVar":      "https://grch38.togovar.org/?mode=simple&term={chromosome}%3A{position}",
        "COSMIC":       "https://cancer.sanger.ac.uk/cosmic/search?q={gene_symbol}+{hgvs_c}",
        "jMorp":        "https://jmorp.megabank.tohoku.ac.jp/search?query={gene_symbol}+{hgvs_p}",
        "OMIM":         "https://www.ncbi.nlm.nih.gov/omim/?term={gene_symbol}",
        "StJude":       "https://pecan.stjude.cloud/variants/proteinpaint?gene={gene_symbol}",
        "JCGA":         "https://www.jcga-scc.jp/ja/gene/{gene_symbol}",
        "OncoKB":       "https://www.oncokb.org/gene/{gene_symbol}",
        "Mastermind":   "https://mastermind.genomenon.com/detail?mutation={gene_symbol}:{hgvs_c}",
        "MyVariants":   "https://myvariant.info/v1/variant/chr{chromosome}:g.{position}{ref}%3E{alt}?assembly=hg38&format=html"
    }

class Constants:
    """その他の定数"""
    TOMMO_PRIMARY_KEYS = ['TOMMO', '60KJPN', '38KJPN', '14KJPN', '8.3KJPN']
    TOMMO_FALLBACK_KEY = 'GnomAD_exomes'


class SummaryViewerF1:
    # Define valid alteration types
    VALID_ALTERATIONS = [
        "MISSENSE",
        "FRAMESHIFT",
        "NONSENSE",
        "SPLICE",
        "NONFRAMESHIFT",
        "FUSION",
        "TRUNCATION",
        "DELETION",
        "DUPLICATION",
        "REARRANGEMENT",
        "AMPLIFICATION",
        "LOSS",
        "OTHER",
    ]
        
    # Custom color map for alterations
    COLOR_MAP = {
        'MISSENSE': '#2ca02c',
        'FRAMESHIFT': '#9467bd',
        'NONSENSE': '#333333',
        'SPLICE': '#e377c2',
        'NONFRAMESHIFT': '#8c564b',
        'FUSION': '#ff7f0e',
        'TRUNCATION': '#7f7f7f',
        'DELETION': '#bcbd22',
        'DUPLICATION': '#17becf',
        'REARRANGEMENT': '#1f77b4',
        'AMPLIFICATION': '#d62728',
        'LOSS': '#1f77b4',
        'OTHER': '#d3d3d3',
        'UNKNOWN': '#d3d3d3',
        '': '#ffffff',
        'male': '#1f77b4',
        'female': '#e377c2',
        'MSI-H': '#ff7f0e',
        'MSI-L': '#c5b0d5',
        'MSS': '#cccccc',
        'TMB Score < 10': '#1f77b4',
        'TMB Score >= 10': '#d62728',
        'FoundationOne': '#ff7f0e',
        'FoundationOne Liquid': '#666666'
    }
       
    # Gene length for x-axis limits
    GENE_LENGTHS = {
        'ABL1': 1130, 'ACVR1B': 505, 'AKT1': 480, 'AKT2': 481, 'AKT3': 479, 'ALK': 1620, 'ALOX12B': 701,
        'AMER1': 1135, 'APC': 2843, 'AR': 920, 'ARAF': 606, 'ARFRP1': 201, 'ARID1A': 2285, 'ASXL1': 1541,
        'ATM': 3056, 'ATR': 2644, 'ATRX': 2492, 'AURKA': 403, 'AURKB': 344, 'AXIN1': 862, 'AXL': 894,
        'BAP1': 729, 'BARD1': 777, 'BCL2': 239, 'BCL2L1': 233, 'BCL2L2': 193, 'BCL6': 706, 'BCOR': 1755,
        'BCORL1': 1785, 'BRAF': 766, 'BRCA1': 1863, 'BRCA2': 3418, 'BRD4': 1362, 'BRIP1': 1249, 'BTG1': 171,
        'BTG2': 158, 'BTK': 659, 'CALR': 417, 'CARD11': 1154, 'CASP8': 479, 'CBFB': 187, 'CBL': 906,
        'CCND1': 295, 'CCND2': 289, 'CCND3': 292, 'CCNE1': 410, 'CD22': 847, 'CD274': 290, 'CD70': 193,
        'CD79A': 226, 'CD79B': 229, 'CDH1': 882, 'CDK12': 1490, 'CDK4': 303, 'CDK6': 326, 'CDK8': 464,
        'CDKN1A': 164, 'CDKN1B': 198, 'CDKN2A': 132, 'CDKN2B': 138, 'CDKN2C': 168, 'CEBPA': 358,
        'CHEK1': 476, 'CHEK2': 543, 'CIC': 2517, 'CRKL': 303, 'CREBBP': 2442, 'CSF1R': 972, 'CSF3R': 836,
        'CTCF': 727, 'CTNNA1': 906, 'CTNNB1': 781, 'CUL3': 768, 'CUL4A': 759, 'CYP17A1': 508, 'DAXX': 740,
        'DDR1': 913, 'DDR2': 855, 'DIS3': 958, 'DNMT3A': 912, 'DOT1L': 1537, 'EED': 441, 'EGFR': 1210,
        'EMSY': 1337, 'EPHA3': 983, 'EPHB1': 984, 'EPHB4': 987, 'EP300': 2414, 'ERBB2': 1255, 'ERBB3': 1342,
        'ERBB4': 1308, 'ERCC4': 916, 'ERG': 479, 'ERRFI1': 462, 'ESR1': 595, 'EZH2': 751, 'FANCA': 1455,
        'FANCC': 558, 'FANCG': 622, 'FANCL': 375, 'FAS': 335, 'FBXW7': 707, 'FGF10': 208, 'FGF12': 181,
        'FGF14': 247, 'FGF19': 216, 'FGF23': 251, 'FGF3': 239, 'FGF4': 206, 'FGF6': 208, 'FGFR1': 822,
        'FGFR2': 822, 'FGFR3': 806, 'FGFR4': 802, 'FH': 510, 'FLCN': 579, 'FLT1': 1338, 'FLT3': 993, 'FOXL2': 376,
        'FUBP1': 644, 'GABRA6': 453, 'GATA3': 444, 'GATA4': 443, 'GATA6': 595, 'GID4': 300, 'GNA11': 359,
        'GNA13': 377, 'GNAQ': 359, 'GNAS': 1037, 'GRM3': 879, 'GSK3B': 420, 'H3-3A': 136, 'HDAC1': 482,
        'HGF': 728, 'HNF1A': 631, 'HRAS': 170, 'HSD3B1': 373, 'ID3': 119, 'IDH1': 414, 'IDH2': 452,
        'IGF1R': 1367, 'IKBKE': 716, 'IKZF1': 519, 'INPP4B': 924, 'IRF2': 349, 'IRF4': 451, 'IRS2': 1338,
        'JAK1': 1154, 'JAK2': 1132, 'JAK3': 1124, 'JUN': 331, 'KDM5A': 1690, 'KDM5C': 1560, 'KDM6A': 1453,
        'KEAP1': 624, 'KDR': 1356, 'KEL': 732, 'KIT': 976, 'KLHL6': 621, 'KMT2A': 3972, 'KMT2D': 5537,
        'KRAS': 188, 'LYN': 512, 'MAF': 403, 'MAP2K1': 393, 'MAP2K2': 400, 'MAP2K4': 399, 'MAP3K1': 1512,
        'MAP3K13': 966, 'MAPK1': 360, 'MDM2': 497, 'MDM4': 490, 'MED12': 2177, 'MEF2B': 368, 'MEN1': 610,
        'MERTK': 999, 'MET': 1390, 'MITF': 419, 'MKNK1': 412, 'MLH1': 756, 'MPL': 635, 'MRE11': 708,
        'MSH2': 934, 'MSH3': 1137, 'MSH6': 1360, 'MST1R': 1400, 'MTAP': 283, 'MTOR': 2549, 'MUTYH': 549,
        'MYC': 454, 'MYCL': 364, 'MYCN': 464, 'MYD88': 296, 'NBN': 754, 'NFE2L2': 605, 'NF1': 2839,
        'NF2': 595, 'NFKBIA': 317, 'NKX2-1': 371, 'NOTCH1': 2555, 'NOTCH2': 2471, 'NOTCH3': 2321,
        'NPM1': 294, 'NRAS': 189, 'NSD2': 1365, 'NSD3': 1437, 'NTRK1': 796, 'NTRK2': 838, 'NTRK3': 839,
        'NT5C2': 561, 'PALB2': 1186, 'PARP1': 1014, 'PARP2': 570, 'PARP3': 533, 'PAX5': 391, 'PBRM1': 1704,
        'P2RY8': 359, 'PDCD1': 288, 'PDCD1LG2': 273, 'PDGFRA': 1089, 'PDGFRB': 1106, 'PDK1': 436,
        'PIK3CA': 1068, 'PIK3CB': 1070, 'PIK3C2B': 1634, 'PIK3C2G': 1486, 'PIK3R1': 724, 'PIM1': 313,
        'PMS2': 862, 'POLE': 2286, 'POLD1': 1107, 'PPP2R1A': 589, 'PPP2R2A': 447, 'PRDM1': 825,
        'PRKAR1A': 381, 'PRKCI': 596, 'PRKN': 465, 'PTCH1': 1446, 'PTEN': 403, 'PTPN11': 593, 'PTPRO': 1216,
        'QKI': 341, 'RAC1': 192, 'RAD21': 631, 'RAD51': 339, 'RAD51B': 350, 'RAD51C': 376, 'RAD51D': 328,
        'RAD52': 418, 'RAD54L': 747, 'RARA': 462, 'RAF1': 648, 'RB1': 928, 'RBM10': 930, 'REL': 587,
        'RET': 1114, 'RICTOR': 1708, 'ROS1': 2341, 'RPTOR': 1335, 'SDHA': 664, 'SDHB': 280, 'SDHC': 169,
        'SDHD': 159, 'SETD2': 2564, 'SF3B1': 1304, 'SGK1': 526, 'SMAD2': 467, 'SMAD4': 552, 'SMARCA4': 1679,
        'SMARCB1': 385, 'SMO': 787, 'SNCAIP': 919, 'SOCS1': 211, 'SOX2': 317, 'SOX9': 509, 'SPEN': 3664,
        'SPOP': 374, 'SRC': 536, 'STAG2': 1268, 'STAT3': 770, 'STK11': 433, 'SUFU': 484, 'TBX3': 723,
        'TEK': 1124, 'TENT5C': 391, 'TET2': 2002, 'TGFBR2': 567, 'TIPARP': 657, 'TNFAIP3': 790,
        'TNFRSF14': 283, 'TP53': 393, 'TSC1': 1164, 'TSC2': 1807, 'TYRO3': 890, 'U2AF1': 240, 'VEGFA': 395,
        'VHL': 213, 'WT1': 522, 'XPO1': 1071, 'XRCC2': 280, 'ZNF217': 1048, 'ZNF703': 590
    }
