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
RUN pip3 install --upgrade pip wheel
RUN pip install python-redmine
RUN pip install python-pptx
RUN pip install python-docx
RUN pip install pdfplumber
RUN pip install openpyxl
RUN pip install xlrd==1.2.0
RUN python3 -m pip install elasticsearch

# RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch analysis-nori
# RUN elasticsearch-plugin install analysis-nori
RUN pip3 install --index-url https://nexus.netand.co.kr/repository/pipy/simple --upgrade pip --user
RUN pip3 install --index-url https://nexus.netand.co.kr/repository/pipy/simple -r ./requirements.txt



