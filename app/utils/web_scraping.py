import re
import requests
from bs4 import BeautifulSoup
import genebe as gnb

from .parameter import Hyperlink



def fetch_genebe(analysis_type, transcript_id, cds_change):

    if analysis_type == 'HemeSight':
        grc = "hg38"
    elif analysis_type == 'FoundationOne':
        grc = "hg19"
    elif analysis_type == 'FoundationOne Liquid':
        grc = "hg19"
    elif analysis_type == 'GenMineTOP':
        grc = "hg38"
    elif analysis_type == 'Guardant360':
        grc = "hg19"
        
    url = f'{Hyperlink.GENEBE_LINK}{grc}/{transcript_id}:{cds_change}'
    
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[GeneBe fetch error] {e} - URL: {url}")
        return None, None, None, None, None, None, None

    soup = BeautifulSoup(r.text, 'html.parser')
    
    try:
        if grc == "hg19":
            variant_element = soup.find('div', class_='prose max-w-none').find("a")
        else:
            variant_element = soup.find('li', class_='inline-block').find("a")
        variant = variant_element.get_text(strip=True).replace('hg38:', '').replace('chr:', '')
        chromosome, position, ref, alt = variant.split('-')
        chromosome = chromosome.replace('chr', '')
        
        genebe_json = gnb.annotate_variants_list([variant], flatten_consequences=False, genome=grc)
        dbsnp = genebe_json[0].get('dbsnp')
    except Exception as e:
        print(f"[GeneBe parsing error] {e} - URL: {url}")
        return None, None, None, None, None, None, None

    return genebe_json, variant, chromosome, position, ref, alt, dbsnp
    

def fetch_tommo(transcript_id, cds_change, alt, dbsnp):
    url = f'{Hyperlink.DBSNP_LINK}{transcript_id}:{cds_change}'
    url_dbsnp = f'{Hyperlink.DBSNP_LINK}{dbsnp}'

    primary_keys = ['TOMMO', '38KJPN', '14KJPN', '8.3KJPN']
    fallback_key = 'GnomAD_exomes'

    def extract_frequency(text, url):
        pattern = re.compile(rf'\b{alt}=(\d\.\d+)[^()]*\((.*?)\)')
        matches = pattern.findall(text)
        
        for value, source in matches:
            if source in primary_keys:
                try:
                    freq = round(float(value) * 100, 2)
                    # return f'=HYPERLINK("{url}", "{freq}%")'
                    return f"{freq}%"
                except:
                    continue
        
        gnomad_pattern = re.compile(rf'\b{alt}=(\d\.\d+)[^()]*\({fallback_key}\)')
        gnomad_matches = gnomad_pattern.findall(text)
        
        if gnomad_matches:
            try:
                value = gnomad_matches[0]
                freq = round(float(value) * 100, 2)
                # return f'=HYPERLINK("{url}", "({freq}%)")'
                return f"{freq}%"
            except:
                pass
        return "-"

    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        supp_section = soup.find(class_="supp")
        if supp_section:
            return extract_frequency(supp_section.get_text(strip=True), url)

        r_dbsnp = requests.get(url_dbsnp)
        r_dbsnp.raise_for_status()
        soup_dbsnp = BeautifulSoup(r_dbsnp.text, 'html.parser')
        supp_section_dbsnp = soup_dbsnp.find(class_="supp")
        if supp_section_dbsnp:
            return extract_frequency(supp_section_dbsnp.get_text(strip=True), url_dbsnp)
    except Exception as e:
        print(f"[ERROR] Could not fetch data: {e}")
    # return f'=HYPERLINK("{url}", "-")'
    return "-"



def fetch_clinvar(transcript_id, gene_symbol, cds_change, dbsnp):
    """Fetch ClinVar data and pathogenicity using Entrez API"""

    if 'delins' in cds_change:
        cds_change = cds_change.split('delins')[0] + 'delins'
    elif 'dup' in cds_change:
        cds_change = cds_change.split('dup')[0] + 'dup'
    elif 'del' in cds_change:
        cds_change = cds_change.split('del')[0] + 'del'
    elif 'ins' in cds_change:
        cds_change = cds_change.split('ins')[0] + 'ins'

    def fetch_clinvar_id(query):
        base_url = Hyperlink.CLINVAR_SEARCH
        params = {
            "db": "clinvar",
            "term": query,
            "retmode": "json"
        }
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching data from ClinVar: {response.status_code}")
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    # まず transcript_id + cds_change で検索
    query = f'"{transcript_id}:{cds_change}"[variant_name]'
    clinvar_ids = fetch_clinvar_id(query)

    # それで見つからなければ dbSNP ID で再検索
    if dbsnp and not clinvar_ids:
        query = f'"{dbsnp}"[dbsnp_id]'
        clinvar_ids = fetch_clinvar_id(query)

    if not clinvar_ids:
        return "", "", "", "", ""

    for clinvar_id in clinvar_ids:
        url = Hyperlink.CLINVAR_SUMMARY
        params = {
            "db": "clinvar",
            "id": clinvar_id,
            "retmode": "json"
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            continue  # 次のIDを試す

        summary = response.json().get("result", {}).get(clinvar_id, {})

        variation_set = summary.get("variation_set", [])
        cdna_change = variation_set[0].get("cdna_change", "NA") if variation_set else "NA"

        if cds_change in cdna_change:
            germline_sig = summary.get("germline_classification", {}).get("description", "NA")
            germline_status = summary.get("germline_classification", {}).get("review_status", "NA")
            somatic_sig = summary.get("oncogenicity_classification", {}).get("description", "NA")
            somatic_status = summary.get("oncogenicity_classification", {}).get("review_status", "NA")
            return germline_sig, germline_status, somatic_sig, somatic_status, clinvar_id

    # 該当するcds_changeがなかった場合でも最後のClinVar IDの情報を返す
    summary = response.json().get("result", {}).get(clinvar_id, {})
    germline_sig = summary.get("germline_classification", {}).get("description", "NA")
    germline_status = summary.get("germline_classification", {}).get("review_status", "NA")
    somatic_sig = summary.get("oncogenicity_classification", {}).get("description", "NA")
    somatic_status = summary.get("oncogenicity_classification", {}).get("review_status", "NA")
    
    return germline_sig, germline_status, somatic_sig, somatic_status, clinvar_id
