# pyvg

a minimal, scriptable genome browser for python

## installation

```sh
# TODO: name is taken on PyPI ... shoot!
# pip install pyvg
```

Until then, clone this repo and run:

```sh
pip install -e .
```

## usage

```py
import pyvg

# set the reference genome
pyvg.ref("mm10")

# set the locus
pyvg.locus("chr17:31,531,100-31,531,259")

# create a browser instance
pyvg.browse("fragments.bed", "10x_cov.bw")
```

![igv.js in Jupyter Notebook](https://github.com/manzt/anywidget/assets/24403730/8aa77384-6d7c-422f-9238-37e06a0272f6)

That's it. By default, `pyvg` infers the track and data-types by file
extension. If a file format has an index file, it must be specified as 
a tuple (remote URLs also work):

```py
pyvg.browse(
  (
    "https://example.com/example.bam",     # data file
    "https://example.com/example.bam.bai"  # index file
  )
)
```

You can use `track` to adjust track properties beyond the defaults:

```py
pyvg.browse(
  pyvg.track("10x_cov.bw", name="10x coverage", autoscale=True),
)
```

Multiple tracks are supported by adding to the `browse` call:

```py
pyvg.browse(
  # track 1
  (
      "https://example.com/example.bam",
      "https://example.com/example.bam.bai"
  ),
  # track 2
  pyvg.track("10x_cov.bw", name="10x coverage", autoscale=True),
  # track 3
  pyvg.track("genes.bed", name="Genes", color="blue"),
)
```

## development

create a virtual environment and and install pyvg in *editable* mode with the
optional development dependencies:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
