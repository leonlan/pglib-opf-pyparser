# pglib-opf-pyparser
## Introduction
The script `load_pglib_opf` reads a power network instance from pglib-opf [1]. It takes
as input a `pglib_opf_*.m` file and returns a pandas `DataFrame` for three tables:
- the bus data
- the generator and generator cost data
- the branch data

Moreover, using `to_network` you can create a networkx graph from the dataframes.

Check [2] for a description of the Data File Format.

## Usage
Make sure to have pandas installed. To verify that all pglib-opf instances are loaded correctly, run the following command on the command line:
```
python3 load_pglib_opf.py
```

## Todos
- [x] Create `networkx` objects;
- [ ] Create `pandapowerNet`;
  - This one is pretty difficult, because pandapower uses different parameters than what Matpower provides. The best way to implement this is by looking at [pandapower.converter.matpower](https://github.com/e2nIEE/pandapower/blob/v2.0.1/pandapower/converter/matpower/from_mpc.py). 
- [ ] Create a parser class;

## References
- [1] Power Grid Lib - Optimal Power Flow (pglib-opf) https://github.com/power-grid-lib/pglib-opf
- [2] MATPOWER manual: Appendix B Data File Format https://matpower.org/docs/MATPOWER-manual.pdf
