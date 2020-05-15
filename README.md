# py-offline

## Run

```
docker-compose up -d \
  --scale writer=2 \
  --abort-on-container-exit \
  --exit-code-from pyoff_main
```


## Configure

  * `PYOFF_URL` - the site page that needs to be crawled and downloaded
  * `PYOFF_DEPTH` - the depth of the crawl. Default is `0`, only the page's
  resources
  * `PYOFF_DESTINATION` - location where the site files are downloaded


## Overview

There are three main components: the `downloader`, the `parser`, and
the `writer`, each described further down. Each of these has its own service
(in `docker-compose` lingo), which can then be scaled out separately, e.g.
two `downloader` instances, three `parser`s, and one `writer`.

These services are *stateless*, and to achieve that, there is a message broker
between them, the `q` service here (RabbitMQ). They only process what they find
in the queues, and then pass it further down the line. The only state they hold
are their running configurations, e.g. which site they are downloading.

The services are also as *dumb* as possible, leaveraging the running host's
scheduling capavilities. Leaving out reconnecting logic makes for (subjectively)
cleaner and (objectively) less code.

## Components

### Downloader

`download(url)` downloads resources (`HTML`, stylesheets, media, etc.) and
enqueues them for processing.

Subscribes to `q_urls`, with `url(url: str, depth: int = 0)`.

Produces to `q_resources`, with
`resource(url: str, depth: int, mimeType: str, contents: str)`.


### Parser

`parse(resource)` processes the contents of the resource, and decides what to
do next.

1. `HTML` documents are scanned for links to same domain; `URL`s are enqueued
to be downloaded
1. Others are enqueued to be writted on the fs.

Subscribes to `q_resources`.

Produces to `q_files`, with `file(name: str, content: str)`.


### Writer

`write(resource)` writes the resource to the filesystem.

Subscribes to `q_files`.
