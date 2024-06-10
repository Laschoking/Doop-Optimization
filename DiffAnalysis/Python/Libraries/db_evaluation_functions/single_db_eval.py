def calculate_pairwise_occurance_within_DB(db):
    term_pairs = dict()
    for file in db.files:
        for row in db.data_rows[file]:
            l = len(row)
            for ind1 in range(l):
                term1 = row[ind1]
                if term1 == '': continue
                ind2 = ind1 + 1

                while ind2 < l :
                    term2 = row[ind2]
                    ind2 += 1
                    if term2 == '' or term1 == term2:
                        continue
                    if (term1, term2) in term_pairs:
                        term_pairs[(term1,term2)] += 1
                    elif (term2, term1) in term_pairs:
                        term_pairs[(term2,term1)] += 1
                    else:
                        term_pairs[(term1,term2)] = 1


    for term_pair in term_pairs:
        if term_pairs[term_pair] > 5:
            print(term_pair, term_pairs[term_pair])
    return