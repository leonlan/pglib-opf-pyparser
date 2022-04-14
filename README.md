# pglib-opf-pyparser
## Introduction
This script reads a power network instance from pglib-opf [1]. It takes
as input a `pglib_opf_*.m` file and returns a pandas `DataFrame` for three tables:
- the bus data
- the generator and generator cost data
- the branch data

Check [2] for a description of the Data File Format.

## Usage
Make sure to have pandas installed. To verify that all pglib-opf instances are loaded correctly, run the following command on the command line:
```
python3 load_pglib_opf.py
```

## Todos
- [ ] Create `pandapowerNet` and `networkx` objects;
- [ ] Create a parser class;

## References
- [1] Power Grid Lib - Optimal Power Flow (pglib-opf) https://github.com/power-grid-lib/pglib-opf
- [2] MATPOWER manual https://matpower.org/docs/MATPOWER-manual.pdf
