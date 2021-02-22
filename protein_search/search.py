from dataclasses import dataclass
from io import StringIO
from typing import Iterator

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner
from Bio.SeqFeature import FeatureLocation
from Bio.SeqRecord import SeqRecord

from protein_search.models import ProteinDatabaseEntry


@dataclass
class SearchResult:
    """
    Dataclass that represents the final results of a search
    query.

    * record_found: the id of the record where the protein was
      found.
    * record_description: The description of the record where the
      protein was found.
    * record_source: The source of the feature.
    * protein_id: The ID of the protein identified in the feature.
    * location: Where the DNA sequence the feature was found.
    """
    record_found: str
    record_description: str
    record_source: str
    protein_id: str
    location: FeatureLocation


def create_aligner() -> PairwiseAligner:
    """
    Creates an aligner that can be used to search for proteins.
    """
    aligner = PairwiseAligner(mode="local")

    # By default we want matches and penalize mismatches.
    aligner.mismatch_score = -1
    aligner.match_score = 1

    # left or right gaps shouldn't count negatively due to the local search.
    aligner.query_left_gap_score = 0
    aligner.query_right_gap_score = 0
    aligner.target_right_gap_score = 0
    aligner.target_left_gap_score = 0

    # Gaps in the middle should count negatively to narrow down the search space.
    aligner.query_internal_gap_score = -1
    aligner.target_internal_gap_score = -1

    return aligner


def fetch_records() -> Iterator[SeqRecord]:
    """
    Returns an iterator that iterates through all records in
    the database.
    """
    for entry in ProteinDatabaseEntry.objects.all():
        handle = StringIO(entry.content)
        yield SeqIO.read(handle, "gb")


def is_protein_feature(feature):
    """
    Introspects `feature` to determine if it a
    protein.

    Currently it only checks the qualifiers looking for a
    'protein_id' key.
    """
    return "protein_id" in feature.qualifiers


def find_protein_features(features):
    """
    Filters `features` for sequences are encode proteins.
    """
    for feature in features:
        if is_protein_feature(feature):
            yield feature


def search(dna_sequence) -> "SearchResult":
    """
    Searches the database for a protein that has
    a feature that has a similar `dna_sequence`.

    The search computes a local alignment score and picks
    one that scores above zero.
    """
    needle = Seq(dna_sequence)

    aligner = create_aligner()

    for record in fetch_records():
        for feature in find_protein_features(record.features):
            extracted_sequence = feature.extract(record.seq)
            score = aligner.score(extracted_sequence, needle)
            if score > 0:
                return SearchResult(
                    record_found=record.name,
                    record_description=record.description,
                    record_source=record.annotations.get("source", "<source unknown>"),
                    protein_id=feature.qualifiers.get("protein_id")[0],
                    location=feature.location,
                )

    return None
