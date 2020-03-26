'''
Akond Rahman 
Mar 26 2020 
Thursday 
Characterizing scripts 
'''
import pandas as pd 
import numpy as np 
from collections import Counter 
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def getFilesWithSameColocations(df_param):
    file_names = np.unique( df_param['FILEPATH'].tolist() )
    file_count = len(file_names) 
    colocate_dict, file_dict  = {}, {}
    for file_name in file_names:
        per_file_df = df_param[df_param['FILEPATH']==file_name]
        icp_list    = per_file_df['TYPE'].tolist()    
        icp_count_dic =  dict( Counter(icp_list) )
        for k_, v_ in icp_count_dic.items():
            if v_  > 1:
                if k_ not in colocate_dict:
                    colocate_dict[k_] = [v_]
                    file_dict[k_]     = [file_name]
                else:
                    colocate_dict[k_] = colocate_dict[k_] + [v_]                    
                    file_dict[k_]     = file_dict[k_] + [file_name]          
    return file_dict 


def getFilesWithDiffColocations(colocation_df):
    diff_file_list = []
    file_names = np.unique( colocation_df['FILEPATH'].tolist() )    
    for file_name in file_names:
        per_file_df = colocation_df[colocation_df['FILEPATH']==file_name]
        icp_list    = per_file_df['TYPE'].tolist()
        icp_dict = dict( Counter(icp_list) )
        if len(icp_list) > 1:
            for k_, v_ in icp_list.items():
                diff_file_list.append( file_name )
    diff_file_list = list( np.unique(diff_file_list) )
    return diff_file_list 

def getColocationMapping(colocation_file, full_file):
    colocation_df = pd.read_csv(colocation_file)
    full_df       = pd.read_csv(full_file) 

    NO_ICP_DF           = full_df[full_df['TOTAL'] < 1 ]
    files_with_no_icps  = np.unique( NO_ICP_DF['FILE_NAME'].tolist()  )

    ONLY_ONE_ICP_DF     = full_df[full_df['TOTAL'] == 1 ]
    files_with_only_one = np.unique( ONLY_ONE_ICP_DF['FILE_NAME'].tolist()  )

    MORE_THAN_ONE_ICP_DF = full_df[full_df['TOTAL'] > 1 ]
    files_with_more_one  = np.unique( MORE_THAN_ONE_ICP_DF['FILE_NAME'].tolist()  )

    SAME_COLOCATION_DICT = getFilesWithSameColocations(colocation_df) 
    files_with_same_colocation = SAME_COLOCATION_DICT.values() 

    files_with_diff_colocation = getFilesWithDiffColocations(colocation_df) 

    only_files_with_diff_colocation =  [z_ for z_ in files_with_diff_colocation if z_ not in files_with_same_colocation]
    print( only_files_with_diff_colocation )

    only_files_with_same_colocation =  [z_ for z_ in files_with_same_colocation if z_ not in files_with_diff_colocation]
    print( only_files_with_same_colocation )

if __name__=='__main__':
    colocation_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/ICP_Localization/RAW_DATASETS/COLOCATION_INPUT_MOZI.csv'
    full_file       = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/ICP_Localization/RAW_DATASETS/V2_ALL_MOZILLA_PUPPET.csv'

    # dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/ICP_Localization/RAW_DATASETS/COLOCATION_INPUT_OSTK.csv'    

    # dataset_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/ICP_Localization/RAW_DATASETS/COLOCATION_INPUT_WIKI.csv'    
    print('~'*100) 
    getColocationMapping(colocation_file, full_file) 
    print('~'*100)     