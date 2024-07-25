from Python.Libraries import Classes
from Python.Libraries import ShellLib
import pandas as pd

# each Mapping has a Strategy and a similarity metric
class Mapping():
    def __init__(self, paths, exp_name,expansion_strategy,sim_name, similarity_metric):
        name = exp_name + "-" + sim_name
        self.name = name

        self.db1_renamed_facts = Classes.DB_Instance(paths.db1_facts,name)

        self.db_merged_facts = Classes.DB_Instance(paths.merge_facts, name)
        self.db_merged_results = Classes.DB_Instance(paths.merge_results, name)

        self.db1_unravelled_results = Classes.DB_Instance(paths.db1_results, name)
        self.db2_unravelled_results = Classes.DB_Instance(paths.db2_results, name)

        self.mapping = pd.DataFrame()
        self.mapping_path = paths.mapping_results.joinpath(self.name).with_suffix('.tsv')
        self.new_term_counter = 0
        self.expansion_strategy = expansion_strategy
        self.similarity_metric = similarity_metric

        self.c_uncertain_mappings = 0
        self.c_hub_recomp = 0
        self.c_comp_tuples = 0

    def set_mapping(self, mapping):
        self.mapping = mapping

    def compute_mapping(self,db1,terms1,db2,terms2,pa_non_mapping_terms):
        uncertain_mapping_tuples, count_hub_recomp, comp_tuples = self.expansion_strategy(self,db1,terms1,db2,terms2,pa_non_mapping_terms,self.similarity_metric)
        self.c_uncertain_mappings = uncertain_mapping_tuples
        self.c_hub_recomp = count_hub_recomp
        self.c_comp_tuples = comp_tuples

        for file_name,df in db1.files.items():
            mapped_df = self.map_df(df, self.mapping[0], self.mapping[1])
            self.db1_renamed_facts.insert_df(file_name,mapped_df)
        return

    def map_df(self, df, from_terms, to_terms):
        # assuming that keys & values are unpacked according to insertion order
        return df.replace(from_terms.to_list(),to_terms.to_list())


    def read_mapping(self):
        if self.mapping_path.exists():
            df = pd.read_csv(self.mapping_path,sep='\t', header=None)
            # check how many terms have been mapped to synthetic term
            self.new_term_counter = df[1].str.startswith("new_var").value_counts()
            self.mapping = df
        else:
            raise FileNotFoundError(self.mapping_path)


    # output stuff
    def log_mapping(self):
        ShellLib.clear_directory(self.mapping_path.parent)
        self.mapping.to_csv(self.mapping_path,sep='\t',index=False,header=False)


# can be implemented faster, just replace db
    def merge_dbs(self,db1,db2,to_db):
        for file_name in db1.files.keys():
            df1 = db1.files[file_name]
            df2 = db2.files[file_name]
            if not df1.empty and not df2.empty:
                l_cols = len(df1.columns)
                cols = list(range(l_cols))
                df = pd.merge(df1,df2,how='outer',on=cols,indicator=str(l_cols))
                df[str(l_cols)] = df[str(l_cols)].astype(str).replace({'both': '0', 'left_only': '1', "right_only": '10'})
            elif not df1.empty:
                l_cols = len(df1.columns)
                df = df1
                df[l_cols] = '1'
            elif not df2.empty:
                l_cols = len(df2.columns)
                df = df2
                df[l_cols] = '10'
            else:
                df = pd.DataFrame()
            to_db.insert_df(file_name,df)


# from_db & to_db are objects of self.mapping, so setting them will modify self.mapping (since its pointers)
    # from_DB is usually db2 & to_db is db1
    def unravel_merge_dbs(self):
        #pa_additionally_terms = set()
        for file_name,df in self.db_merged_results.files.items():
            if not df.empty:
                df0 = df[df.iloc[:,-1] == '0']
                df1 = df[df.iloc[:,-1] == '1']
                df2 = df[df.iloc[:,-1] == '10']
                df1 = pd.concat([df1,df0],axis=0,ignore_index=True)
                df1 = df1.iloc[:,:-1]
                df2 = pd.concat([df2,df0],axis=0,ignore_index=True)
                df2 = df2.iloc[:,:-1]
                # reverse columns of mapping to inverse the mapping
                df1 = self.map_df(df1, self.mapping[1], self.mapping[0])
                self.db1_unravelled_results.insert_df(file_name, df1)
                self.db2_unravelled_results.insert_df(file_name,df2)
            else:
                self.db1_unravelled_results.insert_df(file_name,pd.DataFrame())
                self.db2_unravelled_results.insert_df(file_name, pd.DataFrame())
        return

