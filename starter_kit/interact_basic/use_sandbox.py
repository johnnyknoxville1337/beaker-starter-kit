from beaker import sandbox

# get_accounts method gives the list of sandboxAccount objects 
accts = sandbox.get_accounts()
print(*accts, sep = "\n\n")

# sandboxAccount objects
acct1 = accts.pop()

print(f"acct1 address is {acct1.address}")
print(f"acct1 private key is {acct1.private_key}")
print(f"acct1 signer is {acct1.signer}\n")

# get_algod_client creates a client object by automatically detecting your sandbox configuration
client = sandbox.get_algod_client()
sp = client.suggested_params()
print(f"suggested flat fee is {sp.min_fee} microAlgos")



