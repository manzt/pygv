from __future__ import annotations

import typing as t

from msgspec import UNSET, Struct, UnsetType, field

__all__ = [
    "AlignmentTrack",
    "AnnotationTrack",
    "BaseTrack",
    "Track",
    "VariantTrack",
    "WigTrack",
]


class BaseTrack(Struct, rename="camel", repr_omit_defaults=True, omit_defaults=True):
    """Represents a browser track.

    For a full configuration options, see the [IGV.js docs](https://igv.org/doc/igvjs/#tracks/Tracks)
    """

    associated_file_formats: t.ClassVar[set[str]] = set()
    """File formats associated with this track type."""

    name: str
    """Display name (label). Required."""

    url: str
    """URL to the track data resource, such as a file or webservice, or a data URI."""

    index_url: t.Union[str, UnsetType] = field(default=UNSET, name="indexURL")  # noqa: UP007
    """URL to a file index, such as a BAM .bai, tabix .tbi, or tribble .idx file.

    For indexed file access the index URL is required, if absent the entire file
    will be read.
    """

    source_type: t.Union[t.Literal["file", "htsget", "custom"], UnsetType] = UNSET  # noqa: UP007
    """Type of data source."""

    format: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """No default. If not specified, format is inferred from file name extension."""

    indexed: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Explicitly indicate whether the resource is indexed.

    This flag is redundant if `index_url` is provided. It can be used to load small
    BAM files without an index by setting to `False`
    """

    order: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Integer value specifying relative order of track position on the screen.

    To pin a track to the bottom use a very large value.
    If no order is specified, tracks appear in order of their addition.
    """

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value for track features, e.g. "#ff0000" or "rgb(100,0,100)"."""

    height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Initial height of track viewport in pixels. Default 50."""

    min_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Minimum height of track in pixels. Default 50."""

    max_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum height of track in pixels. Default 500."""

    visibility_window: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum window size in base pairs for which indexed annotations or
    variants are displayed.

    1 MB for variants, 30 KB for alignments, whole chromosome for
    other track types.
    """

    removable: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """If true a "remove" item is included in the track menu. Default `True`."""

    headers: t.Union[dict[str, str], UnsetType] = UNSET  # noqa: UP007
    """HTTP headers to include with each request.

    For example `{"Authorization": "Bearer cn389ncoiwuencr"}`.
    """

    oauth_token: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """OAuth token, or function returning an OAuth token.

    The value will be included as a Bearer token with each request.
    """


class AnnotationTrack(BaseTrack, tag="annotation"):
    """Display views of genomic annotations.

    Associated file formats: bed, gff, gff3, gtf, bedpe (and more).

    Ref: https://igv.org/doc/igvjs/#tracks/Annotation-Track
    """

    associated_file_formats: t.ClassVar[set[str]] = {
        "bed",
        "gff",
        "gff3",
        "gtf",
        "bedpe",
    }
    """File formats associated with the annotation type."""

    display_mode: t.Union[t.Literal["COLLAPSED", "EXPANDED", "SQUISHED"], UnsetType] = (  # noqa: UP007
        UNSET
    )
    """Annotation track display mode. Default `"COLLAPSED"`."""

    expanded_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Height of each row of features in `"EXPANDED"` mode. Default `30`."""

    squished_row_height: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Height of each row of features in `"SQUISHED"` mode. Default `15`."""

    name_field: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """For GFF/GTF file formats. Name of column 9 to be used for feature label."""

    max_rows: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum number of rows of features to display. Default `500`."""

    searchable: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether feature names for this track can be searched. Default `False`.

    Does not work for indexed tracks. Use with caution; it is memory intensive.
    """

    searchable_fields: t.Union[list[str], UnsetType] = UNSET  # noqa: UP007
    """Field (column 9) names to be included in feature searches.

    For use with the `searchable` option in conjunction with GFF files.

    When searching for feature attributes spaces need to be escaped with a "+"
    sign or percent encoded ("%20).
    """

    filter_types: t.Union[list[str], UnsetType] = UNSET  # noqa: UP007
    """GFF feature types to filter from display. Default `["chromosome", "gene"]`."""

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value for features. Default `"rgb(0,0,150)"` (i.e. `"#000096"`)."""

    alt_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """If supplied, used for features on negative strand."""

    color_by: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """Used with GFF/GTF files. Name of column 9 attribute to color features by."""

    color_table: t.Union[dict[str, str], UnsetType] = UNSET  # noqa: UP007
    """Maps attribute values to CSS colors.

    Used in conjunction with the `color_by` to assign specific colors to attributes.

    Example:

    ```py
    AnnotationTrack(
        name="Color by attribute biotype",
        format="gff3",
        display_mode="expanded",
        height=300,
        url="https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz",
        index_url="https://s3.amazonaws.com/igv.org.genomes/hg38/Homo_sapiens.GRCh38.94.chr.gff3.gz.tbi",
        visibility_window=1000000,
        color_by="biotype",
        color_table={
            "antisense": "blueviolet",
            "protein_coding": "blue",
            "retained_intron": "rgb(0, 150, 150)",
            "processed_transcript": "purple",
            "processed_pseudogene": "#7fff00",
            "unprocessed_pseudogene": "#d2691e",
            "*": "black"
        }
    )
    ```
    """


class GuideLine(Struct):
    """Represents a horizontal guide line."""

    color: str
    """A CSS color value."""
    dotted: bool
    """Whether the line should be dashed."""
    y: int
    """The y position. Should be between min and max."""


class WigTrack(BaseTrack, tag="wig"):
    """Displays quantititive data as either a bar chart, line plot, or points.

    Associated file formats: wig, bigWig, bedGraph.

    Ref: https://igv.org/doc/igvjs/#tracks/Wig-Track/
    """

    associated_file_formats: t.ClassVar[set[str]] = {"wig", "bigWig", "bedGraph"}
    """File formats associated with the wig type."""

    autoscale: t.Union[bool, None] = None  # noqa: UP007
    """Autoscale track to maximum value in view."""

    autoscale_group: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """An identifier for an autoscale group.

    Tracks with the same identifier are autoscaled together.
    """

    min: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Minimum value for the data (y-axis) scale. Usually zero."""

    max: t.Union[int, UnsetType] = UNSET  # noqa: UP007
    """Maximum value for the data (y-axis) scale. Ignored if `autoscale` is `True`."""

    color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """CSS color value. Default `"rgb(150,150,150)"`."""

    alt_color: t.Union[str, UnsetType] = UNSET  # noqa: UP007
    """If supplied, used for negative values."""

    color_scale: t.Union[dict, UnsetType] = UNSET  # noqa: UP007
    """Color scale for heatmap (graphType = "heatmap" ).

    Ref: https://igv.org/doc/igvjs/#tracks/Wig-Track/#color-scale-objects
    """

    guide_lines: t.Union[list[GuideLine], UnsetType] = UNSET  # noqa: UP007
    """Draw a horizontal line for each object in the given array."""

    graph_type: t.Union[t.Literal["bar", "points", "heatmap", "line"], UnsetType] = (  # noqa: UP007
        UNSET
    )
    """Type of graph. Default `"bar"`."""

    flip_axis: t.Union[bool, UnsetType] = UNSET  # noqa: UP007
    """Whether the track is drawn "upside down" with zero at top. Default `False`."""

    window_function: t.Union[t.Literal["min", "max", "mean"], UnsetType] = UNSET  # noqa: UP007
    """Governs how data is summarized when zooming out. Default `"mean"`.

    Applicable to tracks created from bigwig and tdf files.
    """


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
