from Bluepay import *


account_id = "Merchant Account ID"
secret_key = "Secret Key"
mode = "TEST"

report = BluePay(
    account_id = account_id,
    secret_key = secret_key,
    mode = mode
)

report.get_transaction_report(
    report_start = '2017-11-20', # Report Start Date: Jan. 1, 2015
    report_end = '2017-11-30', # Report End Date: Aprl. 30, 2015
    subaccounts_searched = '1', # Also search subaccounts? Yes
    do_not_escape = '1', # Output response without commas? Yes
    exclude_errors = '1' # Do not include errored transactions? Yes
)

# Makes the API Request with BluePay
report.process()

# Reads the response from BluePay
print (report.response)