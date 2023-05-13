# PeExports

This simple multithreaded tool is for collecting PE exports to help with API hashing when reverse engineering.

## Output Formats
- JSON
- Pickle

## Install

```batch
git clone https://github.com/c3rb3ru5d3d53c/peexports.git
cd peexports/
pip install .
```

## Examples

```batch
python peexports.py --threads 4 --input C:\Windows\System32\ --recursive --format pickle --output apis.pickle
python peexports.py --threads 4 --input C:\Windows\System32\ --recursive --format json --output apis.json
```
