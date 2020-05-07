# py-offline

```
./py-offline --url=URL --depth=DEPTH --destination=DEST
```

main --> q_documents = [main_page]

for each q_documents, download --> q_downloaded_documents

for each downloaded_documents, parse for links,
  each link --> q_documents, 
  each resource --> q_resources

for each resource, download, write to file (`writer`)

downloaded_doc
-name
-encoding
-body