import contextlib
from typing import List

from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from django.conf import settings

from protein_search.models import ProteinDatabaseEntry


def fetch_entries(identifiers: List[str]) -> List[SeqRecord]:
    """
    Fetches the GenBank nucleotide database for the given identifiers.

    :param identifiers: List of identifiers.
    :return: Returns a list of sequence records.
    """
    Entrez.tool = "MyTestingEntrezTool"
    Entrez.email = settings.ENTREZ_EMAIL
    with contextlib.closing(Entrez.efetch(db="nucleotide", id=",".join(identifiers), rettype="gb", retmode="text")) as handle:
        records = list(SeqIO.parse(handle, "gb"))

    return records


def import_sequences(identifiers: List[str]):
    """
    Imports sequence records with the given identifiers from the
    GenBank nucleotide database.

    :param identifiers: List of identifiers.
    """
    records = fetch_entries(identifiers)

    for record in records:
        try:
            entry = ProteinDatabaseEntry.objects.get(identifier=record.id)
        except ProteinDatabaseEntry.DoesNotExist:
            entry = ProteinDatabaseEntry(identifier=record.id)

        entry.content = record.format("gb")
        entry.save()
