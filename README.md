# pygv

a minimal, scriptable genome browser for python built with [anywidget](https://github.com/manzt/anywidget)

## installation

**Here be dragons 🐉**

```sh
pip install pygv
```

## usage

```py
import pygv

# set the reference genome
pygv.ref("mm10")

# set the locus
pygv.locus("chr17:31,531,100-31,531,259")

# create a browser instance
pygv.browse("fragments.bed", "10x_cov.bw")
```

![igv.js in Jupyter Notebook](https://github.com/manzt/anywidget/assets/24403730/8aa77384-6d7c-422f-9238-37e06a0272f6)

That's it. By default, `pygv` infers the track and data-types by file
extension. If a file format has an index file, it must be specified as 
a tuple (remote URLs also work):

```py
pygv.browse(
  (
    "https://example.com/example.bam",     # data file
    "https://example.com/example.bam.bai"  # index file
  )
)
```

You can use `track` to adjust track properties beyond the defaults:

```py
pygv.browse(
  pygv.track("10x_cov.bw", name="10x coverage", autoscale=True),
)
```

Multiple tracks are supported by adding to the `browse` call:

```py
pygv.browse(
  # track 1
  (
      "https://example.com/example.bam",
      "https://example.com/example.bam.bai"
  ),
  # track 2
  pygv.track("10x_cov.bw", name="10x coverage", autoscale=True),
  # track 3
  pygv.track("genes.bed", name="Genes", color="blue"),
)
```

## development

development requires [uv](https://astral.sh/uv)

```sh
uv run jupyter lab # open notebook with editable install
```

```sh
uv run pytest      # testing
uv run ruff check  # linting
uv run ruff format # formatting
```
