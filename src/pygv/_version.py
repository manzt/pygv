import importlib.metadata

try:
    __version__ = importlib.metadata.version("pygv")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
