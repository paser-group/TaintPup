'''
Akond Rahman 
Dec 09, 2020
Orchestrate parser and graph generator 
'''

import constants 
import parser 
import os 
from collections import Counter 

def getPuppetFiles(path_to_dir):
    valid_  = [] 
    for root_, dirs, files_ in os.walk( path_to_dir ):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if(os.path.exists(full_p_file)):
             if (full_p_file.endswith( constants.PP_EXTENSION  )):
               valid_.append(full_p_file)
    return valid_ 

def finalizeSusps(ls):
    return len(ls) 

def finalizeSwitches( dic_ ): 
    no_default_count = 0 
    for k_, v_ in dic_.items():
        branches = v_[-1]
        default_flag = False 
        for branch_count, branch_content in branches.items():
            if constants.CASE_DEFAULT_KEYWORD in branch_content[-1]:
                default_flag = True 
        if default_flag == False : 
            no_default_count += 1 
    return no_default_count


def sanitizeConfigVals(config_data):
    data_ascii = config_data 
    if(constants.IP_ADDRESS_PATTERN in config_data):
        config_data = config_data.replace(constants.QUOTE_SYMBOL, constants.NULL_SYMBOL)
    elif(  constants.HTTP_PATTERN in config_data ):
        config_data = config_data.replace(constants.WHITESPACE_SYMBOL, constants.NULL_SYMBOL)
    data_value =  config_data.strip() 
    data_ascii = sum([ ord(y_) for y_ in data_value ])     
    return data_ascii



def finalizeInvalidIPs(attr_dict, dict_vars):
    invalid_ip_count = 0 
    output_attrib_dict, output_variable_dict = {}, {}
    for attr_name, attr_data in attr_dict.items():
        attr_value = attr_data[-1]
        attr_ascii = sanitizeConfigVals( attr_value )
        if attr_ascii == 330 or attr_ascii == 425: # 330 is the total of '0.0.0.0', 425  is the total of '0.0.0.0/0'
            invalid_ip_count += 1 
            output_attrib_dict[attr_name] = (attr_value, attr_ascii)  # keeping ascii for debugging in taint tracking 
    for var_name, var_data in dict_vars.items():
        var_value = var_data[-1]
        var_ascii = sanitizeConfigVals( var_value )
        if var_ascii == 330 or var_ascii == 425:  
            invalid_ip_count += 1 
            output_variable_dict[var_name] = (var_value, var_ascii) 
    return invalid_ip_count, output_attrib_dict, output_variable_dict # dict will help in taint tracking 

def finalizeHTTP(attr_dict, dict_vars):
    http_count = 0 
    output_attrib_dict, output_variable_dict = {}, {}
    for attr_name, attr_data in attr_dict.items():
        attr_value = attr_data[-1]
        attr_ascii = sanitizeConfigVals( attr_value )
        if (attr_ascii >= 600) and ( constants.HTTP_PATTERN in attr_value): # 600 is the total of 'http://'
            http_count += 1 
            output_attrib_dict[attr_name] = (attr_value, attr_ascii)  # keeping ascii for debugging in taint tracking 
    for var_name, var_data in dict_vars.items():
        var_value = var_data[-1]
        var_ascii = sanitizeConfigVals( var_value )
        if (var_ascii >= 600) and ( constants.HTTP_PATTERN in var_value): # 600 is the total of 'http://'
            http_count += 1 
            output_variable_dict[var_name] = (var_value, var_ascii) 
    return http_count, output_attrib_dict, output_variable_dict # dict will help in taint tracking 

def finalizeWeakEncrypt(func_dict):
    weak_count  = 0 
    weak_dict   = {}
    for func_count, func_data in func_dict.items():
        func_name = func_data[0] 
        if constants.MD5_KEYWORD in func_name: 
            weak_dict += 1 
            weak_dict[weak_count] = func_name , constants.MD5_KEYWORD            
        elif  constants.SHA1_KEYWORD in func_name:
            weak_dict += 1 
            weak_dict[weak_count] = func_name, constants.SHA1_KEYWORD
    return weak_dict

def checkIfValidSecret(single_config_val):
    flag2Ret = False 
    config_val = single_config_val.strip() 
    if ( any(x_ in config_val for x_ in constants.INVALID_SECRET_CONFIG_VALUES ) ):
        flag2Ret = False 
    else:
        if(  len(config_val) > 0 ) and ( constants.QUOTE_SYMBOL in config_val ) :
            flag2Ret = True 
    return flag2Ret



def finalizeHardCodedSecrets( attr_dict, vars_dict ):
    secret_attr_dict , secret_var_dict = {}, {} 
    for attr_name, attr_data in attr_dict.items():
        attr_value = attr_data[-1]
        attr_name  = attr_name.strip() 
        if(any(x_ in attr_name for x_ in constants.SECRET_PASSWORD_LIST )) and (checkIfValidSecret ( attr_value ) ):        
            secret_attr_dict[attr_name] =  attr_value, constants.OUTPUT_PASS_KW
        elif(any(x_ in attr_name for x_ in constants.SECRET_USER_LIST )) and (checkIfValidSecret ( attr_value ) ) :        
            secret_attr_dict[attr_name] =  attr_value, constants.OUTPUT_USER_KW
        elif(any(x_ in attr_name for x_ in constants.SECRET_KEY_LIST )) and (checkIfValidSecret ( attr_value ) ) :        
            secret_attr_dict[attr_name] =  attr_value , constants.OUTPUT_TOKEN_KW
    for var_name, var_data in vars_dict.items():
        var_value  = var_data[-1]
        var_name   = var_name.strip() 
        if(any(x_ in var_name for x_ in constants.SECRET_PASSWORD_LIST )) and (checkIfValidSecret ( var_value ) ):        
            secret_var_dict[var_name] = var_value, constants.OUTPUT_PASS_KW
        elif(any(x_ in var_name for x_ in constants.SECRET_USER_LIST )) and (checkIfValidSecret ( var_value ) ) :        
            secret_var_dict[var_name] = var_value, constants.OUTPUT_USER_KW 
        elif(any(x_ in var_name for x_ in constants.SECRET_KEY_LIST )) and (checkIfValidSecret ( var_value ) ) :        
            secret_var_dict[var_name] = var_value, constants.OUTPUT_TOKEN_KW
    return secret_attr_dict, secret_var_dict  

def orchestrate(dir_):
    all_pupp_files = getPuppetFiles(  dir_ )
    for pupp_file in all_pupp_files:
        dict_reso, dict_clas, dict_all_attr, dict_all_vari, dict_switch, list_susp_comm, dict_func = parser.executeParser( pupp_file ) 
        susp_cnt       = finalizeSusps( list_susp_comm )
        switch_cnt     = finalizeSwitches( dict_switch )
        invalid_ip_cnt, invalid_ip_dict_attr, invalid_ip_dict_vars  = finalizeInvalidIPs( dict_all_attr, dict_all_vari ) 
        http_cnt , http_dict_attr, http_dict_vars = finalizeHTTP( dict_all_attr, dict_all_vari )
        weak_crypt_dic = finalizeWeakEncrypt( dict_func ) 
        secret_dict_attr, secret_dict_vars = finalizeHardCodedSecrets( dict_all_attr, dict_all_vari )
        total_secret_count = len(secret_dict_attr) + len(secret_dict_vars) 

        print( pupp_file, susp_cnt, switch_cnt , invalid_ip_cnt, http_cnt, len(weak_crypt_dic )  , total_secret_count , secret_dict_vars  )
        print('-'*100)


if __name__=='__main__':
    test_pp_dir = '../puppet-scripts/'
    orchestrate( test_pp_dir )
