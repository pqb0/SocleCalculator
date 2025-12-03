import Ssum
import re



def DirectSumMethod(k, lam, mu):
    muP_list = Ssum.subset_partitions(mu)
    lamP_list = Ssum.subset_partitions(lam)

    string_sol = ""

    for lamP in lamP_list:
        for muP in muP_list:
            S = Ssum.CalcSoc(k, lam, lamP, mu, muP)
            # print(f'lP = {lamP}, mP = {muP}, k = {k}      S = {S}')

            #print(f'S is {S}')
            if S != 0:
                # print("!!\n")
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
    print(f"Table for $\\lambda = {lam}$, $\\mu = {mu}, k = {k}$:\n")

    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{|c|}")
    print("\\hline")

    for i in range(2*k):
        row = DirectSumMethod(k-i, lam, mu)

        if row == f"":
            continue
        #if row == "":
            #row = r"$0$"        # optional: ensure the table cell isn't empty
        print(f"${row}$ \\\\ \\hline")
        

    print(f' $V^{{{lam}, {mu}}}$\\\\ \\hline')
    print("\\end{tabular}")
    print("\\end{table}")



def MakeTable_tex(lam, mu, filename="table.tex"):
    # Build the LaTeX content
    tex = []
    tex1 = []
    tex.append(f"\\renewcommand{{\\arraystretch}}{{1.6}} \n")
    tex.append("\\begin{table}[H]\n")
    tex.append("\\centering\n")
    tex.append(f"\\caption{{Table for $\\lambda = {lam}$, $\\mu = {mu}$:}}\n")
    tex.append("\\begin{tabular}{|>{\\centering\\arraybackslash}p{15cm}|}\n")
    tex.append("\\hline\n")


    k = 0
    while True:
        row = DirectSumMethod(k, lam, mu)
        if row == f"":
            break
        row = re.sub(r"\((\d+),\)", r"(\1)", row)
        tex1.append(f" $k = {k}: \quad {row}$ \\\\ \\hline\n")
        k += 1
    
    tex1.reverse()
    tex += tex1
    tex.append("\\end{tabular}\n")
    tex.append("\\end{table}\n")

    # Join into a single string

    tex_string = "".join(tex)

    # Write to file
    with open(filename, "a") as f:
        f.write(tex_string)
        f.write("\n%---------------------\n")

    print(f"LaTeX table written to {filename}")
    return tex_string




if __name__ == '__main__':

    MakeTable_tex((1,1), (2,), "./tex_tables/t1.tex")
    MakeTable_tex((1,1), (1,), "./tex_tables/t1.tex")
