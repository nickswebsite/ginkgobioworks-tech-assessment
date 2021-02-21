from django.core.exceptions import ValidationError


DNA_NUCLEOTIDE_CODES = {"A", "C", "G", "T"}


class DnaValidator:
    def __call__(self, value):
        if any(code not in DNA_NUCLEOTIDE_CODES for code in value):
            raise ValidationError(f"Nucleotide codes must be one of {DNA_NUCLEOTIDE_CODES}!")
