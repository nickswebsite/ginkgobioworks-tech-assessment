import contextlib

from Bio import Entrez, SeqIO
from django.conf import settings

from protein_search.models import ProteinDatabaseEntry


def fetch_entries(identifiers):
    Entrez.tool = "MyTestingEntrezTool"
    Entrez.email = settings.ENTREZ_EMAIL
    with contextlib.closing(Entrez.efetch(db="nucleotide", id=",".join(identifiers), rettype="gb", retmode="text")) as handle:
        records = list(SeqIO.parse(handle, "gb"))

    return records


def import_identifiers(identifiers):
    records = fetch_entries(identifiers)

    for record in records:
        try:
            entry = ProteinDatabaseEntry.objects.get(identifier=record.id)
        except ProteinDatabaseEntry.DoesNotExist:
            entry = ProteinDatabaseEntry(identifier=record.id)

        entry.content = record.format("gb")
        entry.save()
