from Bluepay import *
##
# BluePay Python Sample code.
#
# This code sample runs a $3.00 CC Sale transaction
# against a customer using test payment information.
##

account_id = "Merchant Account ID"
secret_key = "Secret Key"
mode = "TEST"

payment = BluePay(
    account_id = account_id,
    secret_key = secret_key,
    mode = mode
)

payment.set_customer_information(
    name1 = "Bob",
    name2 = "Tester",
    addr1 = "123 Test St.",
    addr2 = "Apt #500",
    city = "Testville",
    state = "IL",
    zipcode = "54321",
    country = "USA"
)

payment.set_cc_information(
    card_number = "4111111111111111",
    card_expire = "1219",
    cvv2 = "123"
)

payment.sale(amount = '5.00') # Sale Amount: $3.00

# Makes the API Request for processing the sale
payment.process()

# If transaction was approved..
if payment.is_successful_response():
    payment_return = BluePay(
        account_id = account_id, # Merchant's Account ID
        secret_key = secret_key, # Merchant's Secret Key
        mode = mode # Transaction Mode: TEST (can also be LIVE)
    )

    # Creates a refund transaction against previous sale
    payment_return.refund(
        transaction_id = payment.trans_id_response, # id of the transaction to refund
        amount = '3.75' # partial refund of $1.75
    )

# Makes the API Request for processing the sale
    payment_return.process()

if payment.is_successful_response():
    print ('Transaction Status: ' + payment.status_response)
    print ('Transaction Message: ' + payment.message_response)
    print ('Transaction ID: ' + payment.trans_id_response)
    print ('AVS Result: ' + payment.avs_code_response)
    print ('CVV2 Result: ' + payment.cvv2_code_response)
    print ('Masked Payment Account: ' + payment.masked_account_response)
    print ('Card Type: ' + payment.card_type_response)
    print ('Auth Code: ' + payment.auth_code_response)
else:
    print (payment.message_response)

