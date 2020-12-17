'''
Akond Rahman 
Dec 13, 2020 
Constants needed to do testing 
'''

common_error_string = 'DOES NOT MATCH:::Should be '

_multi_taint_script_name    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/onos-dasboard.pp' 
_multi_taint_var_input      = '$password'
_multi_taint_var_output     = '$json_message'
_multi_taint_var_error_msg  = common_error_string + _multi_taint_var_output 

_liveness_script_name    = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/packstack-2018-06/packstack/puppet/modules/packstack/manifests/keystone/gnocchi.pp'
_liveness_var_input_list = [  '$auth_name', '$password', '$public_url', '$admin_url', '$internal_url', '$public_url_s3', '$admin_url_s3', '$internal_url_s3' ]
_liveness_error_msg      = common_error_string + 'TRUE' 

_single_taint_script_name = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/puppet-ec2api-2018-06/manifests/db/postgresql.pp' 
_single_taint_var         = 'user' 
_single_taint_dict_key    = 'user' 
_single_taint_type        = 'USERNAME' 
_single_taint_error_true  = common_error_string + 'TRUE' 
_single_taint_error_msg   = common_error_string + 'user' 
OUTPUT_SECRET_KW          = 'HARD_CODED_SECRET'

_susp_script_name = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/wiki-pupp/puppet-2018-06/manifests/realm.pp' 
_susp_error_msg   = common_error_string + '6'


_missing_default_script_name = 'test.api.pp' 
_missing_default_msg         = common_error_string + '1'
_present_default_script_name = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/params.switch.case.pp'
_present_default_msg         = common_error_string + '0'

_invalid_ip_script_name1 = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/init1.pp' 
_invalid_ip_script_name2 = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/init2.pp' 
_invalid_ip_script_name3 = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/packstack-2018-06/packstack/puppet/modules/packstack/manifests/magnum.pp'
_invalid_ip_msg1         = common_error_string + '1'
_invalid_ip_msg0         = common_error_string + '0'

_http_var_script_name    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/auth.pp' 
_http_msg_1              = common_error_string + '1'
_http_msg_0              = common_error_string + '0'
_http_attr_script_name   = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/onos-dasboard.pp'

_weak_cryp_script_name    = 'test.api.pp' 
_weak_cryp_msg_           = common_error_string + '1'


_empty_pass_script_name    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/oozie.pp' 
_empty_pass_msg_           = common_error_string + '1'

_default_adm_script_name   = 'test.api.pp' 
_default_adm_msg_          = common_error_string + '1'

_secret_script_name   = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/onos-dasboard.pp' 
_secret_msg_          = common_error_string + '2'
_secret_uname         = 'karaf'
_secret_password      = 'karaf'
_secret_flag_status   = 'TRUE'


_username_script_name   = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/IaC/FixFalsePositive/sample-puppet-scripts/manifests/oozie/database/mysql.pp' 

_taintedHttp_script_v1 = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/packstack-2018-06/packstack/puppet/modules/packstack/manifests/keystone/magnum.pp'
_tainted_http_msg_v1   = common_error_string + '3'
_taintedHttp_script_v2 = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/packstack-2018-06/packstack/puppet/modules/packstack/manifests/keystone/manila.pp'
_tainted_http_msg_v2   = common_error_string + '5'
_taintedHttp_script_v3 = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/packstack-2018-06/packstack/puppet/modules/packstack/manifests/keystone/cinder.pp'
_tainted_http_msg_v3   = common_error_string + '9'

OUTPUT_HTTP_KW         = 'INSECURE_HTTP'

_cross_taint_script_1  = '/Users/arahman/PRIOR_NCSU/SECU_REPOS/ostk-pupp/puppet-trove-2018-06/examples/site.pp'
_cross_taint_msg_1     =  common_error_string + '7'