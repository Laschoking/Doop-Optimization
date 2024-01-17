import glob
import os
from Setup import *
from pathlib import Path
import shutil

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

        # run doop for each jar
        os.system("./doop -a  " + PA_NAME + " -i " + jar_path + " --id " + db_name + " --Xfacts-subset APP --cache --generate-jimple")

        if Path(DOOP_OUT_PATH + db_name).exists():
            # copy doop-output to personal workspace
            for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/*.facts"):
                shutil.copy(file, facts_path)

            for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/*.csv"):
                shutil.copy(file, pa_path)

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

