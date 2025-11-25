import main




def DirectSumMethod(k, lam, mu):
    muP_list = main.subset_partitions(mu)
    lamP_list = main.subset_partitions(lam)

    string_sol = ""

    for lamP in lamP_list:
        for muP in muP_list:
            S = main.CalcSoc(k, lam, lamP, mu, muP)

            if S == 0:
                continue


            lamP_str = r"\varnothing" if lamP == () else str(lamP)
            muP_str  = r"\varnothing" if muP == () else str(muP)

            exponent = f"{{{lamP_str}, {muP_str}}}"

            if S == 1:
                term = f"V^{exponent} \\oplus "
            else:
                term = f"{S} V^{exponent} \\oplus "
            
            string_sol += term

    string_sol = string_sol.removesuffix("\\oplus ")
    return string_sol

# Example Use to produce a term in the table
# print(DirectSumMethod(2, (1,1), (1,)))

def MakeTable(k, lam, mu):
    print(f"Table for $\\lambda = {lam}$, $\\mu = {mu}$:\n")

    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{|c|}")
    print("\\hline")

    for i in range(1, k):
        row = DirectSumMethod(i, lam, mu)
        #if row == "":
            #row = r"$0$"        # optional: ensure the table cell isn't empty
        print(f"${row}$ \\\\ \\hline")

    print(f' $V^{{{lam}, {mu}}}$\\\\ \\hline')
    print("\\end{tabular}")
    print("\\end{table}")

# Table Example
# MakeTable(2, (1,1), (1,))

def MakeTable(k, lam, mu, filename="table.tex"):
    # Build the LaTeX content
    tex = []
    tex.append(f"% Automatically generated table\n")
    tex.append(f"Table for $\\lambda = {lam}$, $\\mu = {mu}$:\n")
    tex.append("\\begin{table}[h]\n")
    tex.append("\\centering\n")
    tex.append("\\begin{tabular}{|c|}\n")
    tex.append("\\hline\n")

    for i in range(k):
        row = DirectSumMethod(i, lam, mu)
        if row == "":
            row = r"$0$"
        tex.append(f"{row} \\\\ \\hline\n")

    tex.append("\\end{tabular}\n")
    tex.append("\\end{table}\n")

    # Join into a single string
    tex_string = "".join(tex)

    # Write to file
    with open(filename, "w") as f:
        f.write(tex_string)

    print(f"LaTeX table written to {filename}")
    return tex_string



