def solveOne_new(k, k1, k2, k3, k4):

    if k2 > k1 or k4 > k3:
        return []

    solutions = []


    # !!!!!
    for x1 in range(k + 1):

        print(f'd ={x1}\n')

        max_x2 = math.floor((k - x1)/2)
        print(f'g ={max_x2}\n')
        
        
        
        for x2 in range((max_x2 + 1)):

            if x2 == 0:
                print('skipped')
                continue
                print(23)
            else:
                print('kept going')


                x3 = k1 - k2 - (x1 + x2)
                x4 = k3 - k4 - (x1 + x2)

                print(f'x3: {x3}')
                print(f'x4: {x4}')

                # if x3 == 0 or x4 == 0:
                    #continue

                solutions.append({
                    "deg δ": x1,
                    "deg γ": x2,
                    "p": x3,
                    "q": x4,
                    "deg λ'": k2,
                    "deg μ'": k4
                    
            })


        
    for sol in solutions:
        if sol["deg δ"] + 2 * sol["deg γ"] + sol["p"] + sol["q"] != k:
            solutions.remove(sol)
        elif sol["deg δ"] + sol["deg γ"] + sol["p"] != k1 - k2:
            solutions.remove(sol)
        elif sol["deg δ"] + sol["deg γ"] + sol["q"] != k3 - k4:
            solutions.remove(sol)

    return solutions
