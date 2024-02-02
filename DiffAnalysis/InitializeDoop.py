import glob
import os
from Setup import *
from pathlib import Path
import shutil

# depending on the PA, a big amount of Facts may not be relevant to the PA
# Thus we want to find the subset of fact-relations that is relevant to the current PA

#def reduceFacts():


if __name__ == '__main__':

    # create new folders for facts and program analysis of each db
    os.system("mkdir -p " + MERGE_FACTS_PATH)
    os.system("mkdir -p " + MERGE_PA_PATH)

    dir1 = (JAR1_PATH,JAVA1_PATH,DB1_NAME,FACTS1_PATH,PA1_PATH,JIMPLE1_PATH)
    dir2 = (JAR2_PATH,JAVA2_PATH,DB2_NAME,FACTS2_PATH,PA2_PATH,JIMPLE2_PATH)

    os.chdir(DOOP_PATH)
    for (jar_path, java_path, db_name, facts_path, pa_path, jimple_path) in [dir1, dir2]:
        os.system("mkdir -p " + facts_path)
        os.system("mkdir -p " + pa_path)
        os.system("mkdir -p " + jimple_path)


    # check if Jars exist, otherwise create them
        if not os.path.isfile(jar_path):
            if os.path.isfile(java_path):
                os.system("bin/mkjar " + java_path
                          + " 1.8 " + jar_path)
            else:
                raise FileNotFoundError("The input file does not exist " + db_name)
        # equivalent of switch / case
        match PA_TYPE:
            case PA_TYPES.SOUFFLE_INT:
                # run doop for facts & souffle analysis
                os.system(
                    "./doop -a  " + PA_NAME_SOUFFLE_INT + " -i " + jar_path + " --id " + db_name + " --Xfacts-subset APP --cache --generate-jimple")

                # move PA-Resuls to target directory ( only necessary for souffle_int)
                for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/*.csv"):
                    shutil.copy(file, pa_path)

            case PA_TYPES.SOUFFLE_EXT:
                # run doop for facts only ( PA_name will not be used by doop)
                os.system("./doop -a context-insensitive -i " + jar_path + " --id " + db_name + " --facts-only --Xfacts-subset APP --cache --generate-jimple ")
                # once DOOP generated facts, run souffle 2.1 externally on given PA
                os.system("souffle " + PA_PATH_SOUFFLE_EXT + " -F " + facts_path + " -D " + pa_path + " -j4")


            case PA_TYPES.NEMO:
                # run doop for facts only ( PA_name will not be used by doop)
                os.system("./doop -a  context-insensitive -i " + jar_path + " --id " + db_name + " --facts-only --Xfacts-subset APP --cache --generate-jimple ")

                os.chdir(NEMO_ENGINE_PATH)
                os.system("target/release/nmo " + PA_PATH_NEMO + " -I " + facts_path + " -D " +  pa_path + " --save-results --overwrite-results")
                os.chdir(DOOP_PATH)

        if Path(DOOP_OUT_PATH + db_name).exists():
            # copy doop-output to personal workspace
            for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/*.facts"):
                shutil.copy(file, facts_path)

            for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/jimple/*"):
                shutil.copy(file, jimple_path)

            '''
            if Path(DOOP_OUT_PATH + db_name + "/database/").exists():
                shutil.rmtree(DOOP_OUT_PATH + db_name + "/database/")
        '''        # copy the remainders (meta data from doop to new dir)
            for file in glob.glob(DOOP_OUT_PATH + db_name + "/*"):
                if Path(file).is_file():
                    shutil.copy(file, BASE_PATH + db_name)
            #shutil.rmtree(DOOP_OUT_PATH + db_name)

#     Finished dev [unoptimized + debuginfo] target(s) in 0.13s
#      Running `target/debug/nmo nmo /home/kotname/Documents/Diplom/Code/ex_nemo/Analysis/ClassicDoopAnalysis/ConstantPropagation.rls -I /home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/out/Diff_Example1_Example2/Example1/facts/ -D /home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/out/Diff_Example1_Example2/Example1/results/NEMO/Liveness/ --save-results --overwrite-results`
# [2024-01-22T11:16:45Z ERROR nmo] error: Multiple file support is not yet implemented