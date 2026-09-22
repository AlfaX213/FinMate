from gemini_service import parse_transaction

transaction = parse_transaction("Tadi makan siang 25 ribu")

print(transaction)
print("Type:", transaction.type)
print("Amount:", transaction.amount)
print("Category:", transaction.category)
print("Description:", transaction.description)