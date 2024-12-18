from inline_snapshot import snapshot

from pygv import Config
from pygv._tracks import AlignmentTrack


def test_loads_config():
    config = Config.from_dict(
        {
            "genome": "hg38",
            "locus": "chr8:127,736,588-127,739,371",
            "tracks": [
                {
                    "name": "HG00103",
                    "url": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
                    "indexURL": "https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
                    "format": "cram",
                },
            ],
        },
    )
    assert config == snapshot(
        Config(
            genome="hg38",
            locus="chr8:127,736,588-127,739,371",
            tracks=[
                AlignmentTrack(
                    name="HG00103",
                    url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram",
                    index_url="https://s3.amazonaws.com/1000genomes/data/HG00103/alignment/HG00103.alt_bwamem_GRCh38DH.20150718.GBR.low_coverage.cram.crai",
                    format="cram",
                    indexed=None,
                    color=None,
                    height=50,
                    auto_height=False,
                    min_height=50,
                    max_height=500,
                    visibility_window=None,
                    show_coverage=True,
                    show_alignments=True,
                    view_as_pairs=False,
                    pairs_supported=True,
                    coverage_color="rgb(150, 150, 150)",
                    deletion_color="black",
                    skipped_color="rgb(150, 170, 170)",
                    insertion_color="rgb(138, 94, 161)",
                    neg_strand_color="rgba(150, 150, 230, 0.75)",
                    pos_strand_color="rgba(230, 150, 150, 0.75)",
                    pair_connector_color=None,
                    color_by="unexpectedPair",
                    color_by_tag=None,
                    bam_color_tag="YC",
                    sampling_window_size=100,
                    sampling_depth=100,
                    alignment_row_height=14,
                    readgroup=None,
                    sort=None,
                    show_soft_clips=False,
                    show_mismatches=True,
                    show_insertion_text=False,
                    insertion_text_color="white",
                    show_deletion_text=False,
                    deletion_text_color="black",
                    pair_orientation=None,
                    min_tlen=None,
                    max_tlen=None,
                    min_tlen_percentile=0.1,
                    max_tlen_percentile=99.9,
                ),
            ],
        ),
    )
