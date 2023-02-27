from elasticsearch import Elasticsearch


eshost = '10.198.16.124'
es = Elasticsearch([eshost], port=9200)

query = {
}

result = es.search(index="math_item_engine", body=query)
print(result)
for hit in result['hits']['hits']:
    print(hit['_source'])
