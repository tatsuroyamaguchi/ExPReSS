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
