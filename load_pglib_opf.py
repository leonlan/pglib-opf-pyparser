import pandas as pd
import io
import re


def load_pglib_opf(path):
    """
    Load an pglib_opf instance as a pandapower network.
    """

    with open(path, "r") as fi:
        tables = {}
        flag = False

        for line in fi.read().splitlines():

            # Start of each table
            if line.startswith("%% "):
                flag = True
                name = line.lstrip("%% ")
                tables[name] = []

            # End of each table
            elif line.startswith("];"):
                flag = False

            # Process the contents of each table
            elif flag:

                # Header data
                if line.startswith("% "):
                    headers = remove_empty(line[1:].split(""))
                    tables[name].append(headers)

                # Row data
                elif not line.startswith("mpc."):
                    data = remove_empty(re.split("\s+|;|%+", line))
                    tables[name].append(data)

    # Parse each table and transform into a dataframe
    bus_data = parse_bus_data(tables["bus data"])
    gen_data = parse_generator_data(
        tables["generator data"], tables["generator cost data"]
    )
    branch_data = parse_branch_data(tables["branch data"])
    return [bus_data, gen_data, branch_data]


def to_networkx(bus_data, gen_data, branch_data):
    """
    Makes a networkx instance from the passed-in data.
    """
    import networkx as nx

    G = nx.from_pandas_edgelist(
        branch_data,
        source="fbus",
        target="tbus",
        edge_attr=True,
        create_using=nx.MultiDiGraph,
        edge_key="line_idx",
    )

    busdict = bus_data.set_index("bus_i").T.to_dict()

    # We add an extra attribute 'generator_data' dict to each bus
    # which is empty of there is no generator
    gendict = gen_data.set_index("bus").T.to_dict()
    for key, data in busdict.items():
        data["generator_data"] = gendict.get(key, {})

    nx.set_node_attributes(G, busdict)

    return G


# --------------------------------Utils------------------------------------


def remove_empty(L):
    return list(filter(None, L))


def parse_bus_data(rows):
    return infer_types(pd.DataFrame(columns=rows[0], data=rows[1:]))


def parse_generator_data(generator_rows, generator_cost_rows):
    # Some data instances contain generator types as a comment, i.e., ";NG"
    # but this is not contained in the header.
    has_gen_type = len(generator_rows[0]) + 1 == len(generator_rows[1])
    headers = generator_rows[0] + (["generator_type"] if has_gen_type else [])

    # We determine how many cost coefficients are given
    # and create the corresponding headers
    n = int(generator_cost_rows[1][3])
    headers += generator_cost_rows[0][:4] + [f"c({n-1-i})" for i in range(n)]

    # Concatenate the generator and generator cost rows
    # but ignore the generator type from generator cost is it is there
    data_rows = [
        generator_rows[i]
        + (generator_cost_rows[i][:-1] if has_gen_type else generator_cost_rows[i])
        for i in range(1, len(generator_rows))
    ]

    return infer_types(pd.DataFrame(columns=headers, data=data_rows, dtype=object))


def parse_branch_data(rows):
    df = pd.DataFrame(columns=rows[0], data=rows[1:])
    df["line_idx"] = df.index
    return infer_types(df)


def infer_types(df):
    """
    # HACK: Infer the correct types from the dataframe. Currently, the provided
    pandas methods (df.convert_types, df.infer_types) do not work. The workaround
    is to convert to csv, then read as csv again.
    """
    return pd.read_csv(io.StringIO(df.to_csv(index=False)))


if __name__ == "__main__":
    """
    Test loading all pglib_opf_*.m instances.
    Assumes that all the instances are in the pglib-opf directory.
    """
    import glob

    failure = 0
    for filename in glob.iglob("./" + "**/*.m", recursive=True):
        try:
            _ = load_pglib_opf(filename)
        except Exception as e:
            failure += 1
            print(Exception)
            print(f"Failed loading {filename}")

    if failure == 0:
        print("Succesfully loaded all instances.")
