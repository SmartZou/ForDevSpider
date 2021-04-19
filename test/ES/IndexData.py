from elasticsearch import Elasticsearch

es_index_name = "csdn_index"
es = Elasticsearch(
    ["127.0.0.1:9200"],
    sniff_on_start=False,  # 连接前测试
    sniff_on_connection_fail=True,  # 节点无响应刷新节点
    sniff_timeout=60,  # 设置超时时间
    # 除指定Es地址外，其他值均可以使用默认值
)
_index_mappings = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "source": {
                "type": "text",
                "index": True
            },
            "title": {
                "type": "text",
                "index": True
            },
            "author": {
                "type": "text",
                "index": True
            },
            "updated": {
                "type": "text",
                "index": True
            },
            "tags": {
                "type": "text",
                "index": True
            },
            "content": {
                "type": "text",
                "index": True
            },
        }
    }

}

# 创建索引
# if es.indices.exists(index=es_index_name) is not True:
#     res = es.indices.create(index=es_index_name)
#     print(res)

# 添加数据
doc = {
    'source': "http://www.baidu.com",
    'title': "测试数据",
    'author': "Smart Zou",
    'updated': "2020-20-20",
    'tags': '测试',
    'content': '测试内容',
}
# es.index(index=es_index_name, body=doc, doc_type="csdn")
#
# 删除索引
es.indices.delete('github')