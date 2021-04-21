
#
# def publish_result( self, exception, result ):
#     """
#         Publishes the result to output/analytics stream
#     """
#     pass
#
#
# def perform_healing( self, steps ):
#     """
#         Performs healing mechanism for the exception occured
#     """
#     pass
#
#
# def query_resolution( self, exception, exception_type ):
#     """
#         Queries to Elastic search for getting the healing resolution steps
#     """
#     pass
#
#
# def predict( self, exception ):
#     """
#     Classifies type of exception and performs the resolution steps
#
#     Returns:
#     --------
#         bool - True is successful classification else false
#     """
#     try:
#
#         exception_type = self.classify_exception( exception )
#         self.publish_result( exception, EXCEPT_MAPPING.get( exception_type ) )
#         steps = self.query_resolution( exception, exception_type )
#         self.perform_healing( steps )
#
#     except Exception as e:
#         return False
#
#     return True
