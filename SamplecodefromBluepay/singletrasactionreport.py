from Bluepay import *


account_id = "Merchant Account ID"
secret_key = "Secret Key"
mode = "TEST"

report = BluePay(
    account_id = account_id,
    secret_key = secret_key,
    mode = mode
)

report.get_single_trans_query(
    transaction_id = '100500371306', # Transaction ID
    report_start = "2017-11-20", # Query Start Date: Jan. 1, 2013
    report_end = "2017-11-23", # Query End Date: Jan. 15, 2015
    exclude_errors =  "1" # Do not include errored transactions? Yes
 )

# Makes the API Request with BluePay
report.process()

# Reads the response from BluePay
print (report.response)