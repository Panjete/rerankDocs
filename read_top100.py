## Returns an array of array of tuples
## element at ith position is the array of top100 tuples
## Tuple entries being (Qnum, CORDid, Rank, Score)
def rt100(filename):
    with open(filename, "r") as f:
        file_content = f.read()

    all_q100 = []
    lines = file_content.splitlines()
    n_lines = len(lines) - (len(lines) % 100)

    for i in range(0, n_lines, 100):
        thisQ = []
        for j in range(i, i+100):
            curline = lines[j]
            words = curline.split()
            if(len(words)!= 6):
                print(words)
            ## 0       1       2         3      4        5
            ##Qnum    ign     cordid   rank relevance   ign
            relevant_tuple = (words[0], words[2], words[3], words[4])
            thisQ.append(relevant_tuple)
        all_q100.append(thisQ)
    return all_q100


# t40t100 = rt100("t40-top-100.txt")
# print("num of queries = " , len(t40t100))
# print("first Queries first entry = ", t40t100[0][0])
