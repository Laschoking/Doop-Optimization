import csv

from Setup import *



if __name__=="__main__":
    match PA_TYPE:
        #case PA_TYPES.SOUFFLE_INT:
            #
            #
        #case PA_TYPES.SOUFFLE_EXT:
            #
        case PA_TYPES.NEMO:
            with open(PA_PATH_NEMO, 'r') as pa_nemo, open(PA_RELEVANT_FACT_FILES, 'w+') as rel_facts:
                fact_writer = csv.writer(rel_facts,delimiter=',')
                for line in pa_nemo:
                    if line.__contains__("source") or line.__contains__("import"):
                        relevant_fact = line.split("\"")[1]
                        print(relevant_fact)
                        fact_writer.writerow(relevant_fact)
