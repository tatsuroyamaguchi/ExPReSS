def dna(ref, alt, strand):
    if strand == "+":
        return ref, alt
    elif strand == "-":
        # Reverse complement the reference and alternate alleles
        ref = ref[::-1].translate(str.maketrans("ACGT", "TGCA"))
        alt = alt[::-1].translate(str.maketrans("ACGT", "TGCA"))
        return ref, alt
    else:
        raise ValueError("Strand must be either '+' or '-'")
    

def one_to_three_letter(amino_acids_change):
    """
    アミノ酸の1文字記号を3文字記号に変換する関数
    
    Args:
        one_letter_code (str): 1文字のアミノ酸記号
    
    Returns:
        str: 3文字のアミノ酸記号、該当しない場合はNone
    """
    amino_acid_dict = {
        'A': 'Ala',  # Alanine
        'C': 'Cys',  # Cysteine
        'D': 'Asp',  # Aspartic acid
        'E': 'Glu',  # Glutamic acid
        'F': 'Phe',  # Phenylalanine
        'G': 'Gly',  # Glycine
        'H': 'His',  # Histidine
        'I': 'Ile',  # Isoleucine
        'K': 'Lys',  # Lysine
        'L': 'Leu',  # Leucine
        'M': 'Met',  # Methionine
        'N': 'Asn',  # Asparagine
        'P': 'Pro',  # Proline
        'Q': 'Gln',  # Glutamine
        'R': 'Arg',  # Arginine
        'S': 'Ser',  # Serine
        'T': 'Thr',  # Threonine
        'V': 'Val',  # Valine
        'W': 'Trp',  # Tryptophan
        'Y': 'Tyr',  # Tyrosine
    }
    
    return amino_acid_dict.get(amino_acids_change.upper())

