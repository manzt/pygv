from __future__ import annotations

import typing

import msgspec

__all__ = [
    "AlignmentTrack",
    "AnnotationTrack",
    "BaseTrack",
    "Track",
    "VariantTrack",
    "WigTrack",
]


class BaseTrack(msgspec.Struct, rename="camel"):
    """Represents a browser track.

    Only the minimal set of properties are included here. For a full list of
    properties see the IGV.js documentation at https://github.com/igvteam/igv.js/wiki/Tracks-2.0.
    """

    # Display name (label). Required.
    name: str

    # URL to the track data resource, such as a file or webservice, or a data URI.
    url: str

    # URL to a file index, such as a BAM .bai, tabix .tbi, or tribble .idx file.
    # Notes: For indexed file access the index URL is required, if absent the entire
    # file will be read.
    index_url: typing.Union[str, None] = msgspec.field(default=None, name="indexURL")  # noqa: UP007

    # No default. If not specified, format is inferred from file name extension.
    format: typing.Union[str, None] = None  # noqa: UP007

    # Flag provided to explicitly indicate the resource is not indexed.
    # If a resource is indexed the indexURL should be provided in which case
    # this flag is redundant. This flag can be used to load small BAM files
    # without an index by setting to false.
    indexed: typing.Union[bool, None] = None  # noqa: UP007

    # CSS color value for track features, e.g. "#ff0000" or "rgb(100,0,100)".
    color: typing.Union[str, None] = None  # noqa: UP007

    # Initial height of track viewport in pixels. Defaults to 50.
    height: int = 50

    # If true, then track height is adjusted dynamically, within the bounds set by
    # minHeight and maxHeight, to accommodate features in view. Defaults to False.
    auto_height: bool = False

    # Minimum height of track in pixels. Defaults to 50.
    min_height: int = 50  # Maximum height of track in pixels. Defaults to 500.
    max_height: int = 500

    # Maximum window size in base pairs for which indexed annotations or variants
    # are displayed. 1 MB for variants, 30 KB for alignments, whole chromosome for
    # other track types.
    visibility_window: typing.Union[int, None] = None  # noqa: UP007


class AnnotationTrack(BaseTrack, tag="annotation"):
    """Represents non-quantitative genome annotations such as genes.

    Associated file formats: bed, gff, gff3, gtf, bedpe (and more).

    Ref: https://github.com/igvteam/igv.js/wiki/Annotation-Track
    """

    # Annotation track display mode.
    display_mode: typing.Literal["COLLAPSED", "EXPANDED", "SQUISHED"] = "COLLAPSED"

    # Height of each row of features in "EXPANDED" mode.
    expanded_row_height = 30

    # Height of each row of features in "SQUISHED" mode
    squished_row_height = 15

    # For GFF/GTF file formats. Name of column 9 property to be used for feature label.
    name_field: typing.Union[str, None] = None  # noqa: UP007

    # Maximum number of rows of features to display.
    max_rows: int = 500

    # If true, feature names for this track can be searched for. Use this option with
    # caution, it is memory intensive. This option will not work with indexed tracks.
    searchable: bool = False

    # For use with the searchable option in conjunction with GFF files.
    # An array of field (column 9) names to be included in feature searches.
    # When searching for feature attributes spaces need to be escaped with a "+"
    # sign or percent encoded ("%20).
    searchable_fields: typing.Union[list[str], None] = None  # noqa: UP007

    # Array of gff feature types to filter from display.
    filter_types: list[str] = msgspec.field(
        default_factory=lambda: ["chromosome", "gene"],
    )

    # CSS color value for track features, e.g. "#ff0000" or "rgb(100,0,100)".
    color = "rgb(0,0,150)"

    # If supplied, used for features on negative strand.
    alt_color: typing.Union[str, None] = None  # noqa: UP007

    # Used with GFF/GTF files. Name of column 9 attribute to color features by.
    color_by: typing.Union[str, None] = None  # noqa: UP007


class WigTrack(BaseTrack, tag="wig"):
    """Quantitative genomic data, such as ChIP peaks and alignment coverage.

    Associated file formats: wig, bigWig, bedGraph.

    Ref: https://github.com/igvteam/igv.js/wiki/Wig-Track
    """

    # Autoscale track to maximum value in view
    autoscale: typing.Union[bool, None] = None  # noqa: UP007

    # Identifier for an autoscale group. Tracks with the same identifier are
    # autoscaled together.
    autoscale_group: typing.Union[str, None] = None  # noqa: UP007

    # Sets the minimum value for the data (y-axis) scale. Usually zero.
    # min: int = 0  # noqa: ERA001

    # Sets the maximum value for the data (y-axis) scale. Ignored if autoscale = true.
    # max: int | None = None  # noqa: ERA001

    # Track color as as an "rgb(,,,)" string, a hex string, or css color name.
    color = "rgb(150,150,150)"

    # If supplied, used for negative values. See description of color field above.
    alt_color: typing.Union[str, None] = None  # noqa: UP007

    # Draw a horizontal line for each object in the given array:
    #   guide lines: [ {color: [color], y: [number], dotted: [bool]} ]
    #   Note: y value should be between min and max or it will not show.
    # guide_lines: list[dict] = []  # noqa: ERA001

    # Type of graph, either "bar" or "points"
    graph_type: typing.Literal["bar", "points"] = "bar"

    # If true, track is drawn "upside down" with zero at top
    flip_axis: bool = False

    # Applicable to tracks created from bigwig and tdf files. Governs how data is
    # summarized when zooming out.
    window_function: typing.Literal["min", "max", "mean"] = "mean"


class AlignmentTrack(BaseTrack, tag="alignment"):
    """Represents alignment data such as BAM files.

    Associated file formats: bam, cram.

    Ref: https://github.com/igvteam/igv.js/wiki/Alignment-Track
    """

    # Show coverage depth track.
    show_coverage: bool = True

    # Show individual alignments.
    show_alignments: bool = True

    # If true, paired reads are drawn connected with a line.
    view_as_pairs: bool = False

    # If false, mate information in paired reads is ignored during downsampling.
    pairs_supported: bool = True

    # Color of coverage track.
    coverage_color: str = "rgb(150, 150, 150)"

    # Default color of alignment blocks.
    color = "rgb(170, 170, 170)"

    # Color of line representing a deletion.
    deletion_color: str = "black"

    # Color of line representing a skipped region (e.g., splice junction).
    skipped_color: str = "rgb(150, 170, 170)"

    # Color of marker for insertions.
    insertion_color: str = "rgb(138, 94, 161)"

    # Color of alignment on negative strand. Applicable if colorBy = "strand".
    neg_strand_color: str = "rgba(150, 150, 230, 0.75)"

    # Color of alignment or position strand. Applicable if colorBy = "strand".
    pos_strand_color: str = "rgba(230, 150, 150, 0.75)"

    # Color of connector line between read pairs ("view as pairs" mode).
    pair_connector_color: typing.Union[str, None] = None  # noqa: UP007

    # Alignment color option: one of "none", "strand", "firstOfPairStrand",
    # "pairOrientation", "tlen", "unexpectedPair", or "tag".
    color_by: str = "unexpectedPair"

    # Specific tag to color alignment by.
    color_by_tag: typing.Union[str, None] = None  # noqa: UP007

    # Specifies a special tag that explicitly encodes an r,g,b color value.
    bam_color_tag: str = "YC"

    # Window (bucket) size for alignment downsampling in base pairs.
    sampling_window_size: int = 100

    # Number of alignments to keep per bucket.
    sampling_depth: int = 100

    # Height in pixels of an alignment row when in expanded mode.
    alignment_row_height: int = 14

    # Readgroup ID value (tag 'RG').
    readgroup: typing.Union[str, None] = None  # noqa: UP007

    # Initial sort option. Supports various sorting strategies including by base,
    # strand, insert size, etc.
    sort: typing.Union[str, None] = None  # noqa: UP007

    # Show soft-clipped regions.
    show_soft_clips: bool = False

    # Highlight alignment bases which do not match the reference.
    show_mismatches: bool = True

    # Show number of bases for insertions inline when zoomed in.
    show_insertion_text: bool = False

    # Color for insertion count text.
    insertion_text_color: str = "white"

    # Show number of bases deleted inline when zoomed in.
    show_deletion_text: bool = False

    # Color for deletion count text.
    deletion_text_color: str = "black"

    # Expected orientation of pairs, one of ff, fr, or rf.
    pair_orientation: typing.Union[str, None] = None  # noqa: UP007

    # Minimum expected absolute "TLEN" value.
    min_tlen: typing.Union[int, None] = None  # noqa: UP007

    # Maximum expected absolute "TLEN" value.
    max_tlen: typing.Union[int, None] = None  # noqa: UP007

    # The percentile threshold for expected insert size.
    min_tlen_percentile: float = 0.1

    # The percentile maximum for expected insert size.
    max_tlen_percentile: float = 99.9


class VariantTrack(BaseTrack, tag="variant"):
    """Represents variant data such as VCF files.

    Associated file formats: vcf.

    Ref: https://github.com/igvteam/igv.js/wiki/Variant-Track
    """

    # Display mode. 'COLLAPSED' => show variants only,
    # 'SQUISHED' and 'EXPANDED' => show calls.
    display_mode: typing.Literal["COLLAPSED", "EXPANDED", "SQUISHED"] = "EXPANDED"
    # Height of genotype call rows in SQUISHED mode.
    squished_call_height: int = 1
    # Height of genotype call rows in EXPANDED mode
    expanded_call_height: int = 10


Track = typing.Union[AnnotationTrack, WigTrack, AlignmentTrack, VariantTrack]
