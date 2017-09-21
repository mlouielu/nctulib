from nctulib import NCTULibrary

n = NCTULibrary()
result = n.search(q='unix')
print(len(result))
for i in result:
    print(i.title)
    print(i.url)
