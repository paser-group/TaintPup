import graph
import unittest 
import _test_constants
import parser 
import orchestra 

'''
Note to self: 
everytime we use var_tracker_list from `graph` , we need to clear this list as it is global ... code in graph.py does not clear it 
'''

class TestTaintGraph( unittest.TestCase ):


    def testMultiLevelTaint( self ): 
        _, _, _, dict_of_all_variables, _, _ , _ = parser.executeParser( _test_constants._multi_taint_script_name )
        sink_var =  graph.doMultipleTaint( _test_constants._multi_taint_var_input ,  dict_of_all_variables ) 
        self.assertEqual(  sink_var , _test_constants._multi_taint_var_output, _test_constants._multi_taint_var_error_msg) 
        graph.var_tracker_list.clear() 

    def testLiveness(self):
        _, _, _, dict_of_all_variables, _, _ , _ = parser.executeParser( _test_constants._liveness_script_name )
        for var2test in _test_constants._liveness_var_input_list:
            self.assertTrue( graph.checkLiveness( var2test, dict_of_all_variables ) ,_test_constants._liveness_error_msg  )
    
    def testUnameVarInTaintDict(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._single_taint_script_name ) 
        _, secret_dict_vars =  orchestra.finalizeHardCodedSecrets( dict_all_attr, dict_all_vari )  
        self.assertTrue( checkVarInSmellDict( secret_dict_vars ) , _test_constants._single_taint_error_true)
        graph.var_tracker_list.clear()        

    def testUnameTypeInTaintDict(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._single_taint_script_name ) 
        _, secret_dict_vars =  orchestra.finalizeHardCodedSecrets( dict_all_attr, dict_all_vari )  
        self.assertTrue( getTypeFromSmellDict( secret_dict_vars ) ,  _test_constants._single_taint_error_msg ) 
        graph.var_tracker_list.clear()

    def testUnameTaintDict(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._single_taint_script_name ) 
        _, secret_dict_vars =  orchestra.finalizeHardCodedSecrets( dict_all_attr, dict_all_vari )  
        secret_taint_dict = graph.trackTaint( _test_constants.OUTPUT_SECRET_KW, secret_dict_vars, dict_all_attr, dict_all_vari )
        self.assertTrue( _test_constants._single_taint_dict_key in  secret_taint_dict , _test_constants._single_taint_error_true)        
        graph.var_tracker_list.clear()        

    def testTaintedHTTP_V1(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._taintedHttp_script_v1 ) 
        _, http_dict_vars =  orchestra.finalizeHTTP( dict_all_attr, dict_all_vari ) 
        http_taint_dict = graph.trackTaint( _test_constants.OUTPUT_HTTP_KW, http_dict_vars, dict_all_attr, dict_all_vari )
        self.assertEqual( 3 , len(http_taint_dict['$magnum_protocol']) , _test_constants._tainted_http_msg_v1)         
        graph.var_tracker_list.clear()        


    def testTaintedHTTP_V2(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._taintedHttp_script_v2 ) 
        _, http_dict_vars =  orchestra.finalizeHTTP( dict_all_attr, dict_all_vari )  
        http_taint_dict = graph.trackTaint( _test_constants.OUTPUT_HTTP_KW, http_dict_vars, dict_all_attr, dict_all_vari )
        self.assertEqual( 6 , len(http_taint_dict['$manila_protocol']) , _test_constants._tainted_http_msg_v2)         

    def testTaintedHTTP_V3(self):            
        _, _, dict_all_attr, dict_all_vari, _, _, _ = parser.executeParser( _test_constants._taintedHttp_script_v3 ) 
        _, http_dict_vars =  orchestra.finalizeHTTP( dict_all_attr, dict_all_vari )  
        http_taint_dict = graph.trackTaint( _test_constants.OUTPUT_HTTP_KW, http_dict_vars, dict_all_attr, dict_all_vari )
        self.assertEqual( 9 , len(http_taint_dict['$cinder_protocol']) , _test_constants._tainted_http_msg_v3)         

def checkVarInSmellDict(  dic_smell  ):
        status = False
        for var_cnt, var_data in dic_smell.items():
            name, value, type_ = var_data
            if ( name == _test_constants._single_taint_var ): 
                status = True 
        return status 

def getTypeFromSmellDict( dic_smell ):
        status = False
        for var_cnt, var_data in dic_smell.items():
            name, value, type_ = var_data
            if ( type_ == _test_constants._single_taint_type ): 
                status = True 
        return status 

if __name__ == '__main__':
    unittest.main()