from parser import parse_query

query = "1 kg sugar near my location-dwarka sec 13,delhi at lowest price"

result = parse_query(query)

print(result)