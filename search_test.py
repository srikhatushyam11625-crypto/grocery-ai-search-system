from parser import parse_query
from search import search_grocery

query = "1 kg sugar near my location-dwarka sec 13,delhi at lowest price"

parsed = parse_query(query)

results = search_grocery(parsed)

print(results)