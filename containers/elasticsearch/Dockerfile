FROM docker.elastic.co/elasticsearch/elasticsearch:7.17.2

RUN /bin/sh -c "./bin/elasticsearch-plugin list | grep -q analysis-nori || ./bin/elasticsearch-plugin install analysis-nori"

