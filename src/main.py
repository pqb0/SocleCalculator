import diagrams_tex as diag
import Ssum


filename = "./tex_tables/t2.tex"


def generateTables(n, m, file=filename):
    lam_list = list(Ssum.generate_partitions(n))
    mu_list = list(Ssum.generate_partitions(m))

    
    print(f'For $|\\lambda| = {n}$ and $|\\mu| = {m}$:\n')
    
    for lam in lam_list:
        for mu in mu_list:
            diag.MakeTable_tex(lam, mu, file)
        


if __name__ == '__main__':
    n = 7
    generateTables(n, n, filename)


