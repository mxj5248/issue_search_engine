# --- Dependency ---
FROM python:3.8-slim-buster 
RUN python --version
RUN apt-get update
RUN apt-get install nano
RUN mkdir wd
WORKDIR wd
COPY ./requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install pymysql
RUN pip install IPython
RUN pip3 install argon2-cffi
RUN pip3 install elasticsearch
RUN pip3 install apscheduler
RUN python3 -m pip install elasticsearch

# RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch analysis-nori
# RUN elasticsearch-plugin install analysis-nori
RUN pip3 install --index-url https://nexus.netand.co.kr/repository/pipy/simple --upgrade pip --user
RUN pip3 install --index-url https://nexus.netand.co.kr/repository/pipy/simple -r ./requirements.txt

## bin nori 설치 하기 
# // 노리 플러그인 설치
# bin/elasticsearch-plugin install analysis-nori


