# --------------------------
# Docker file
# --------------------------
FROM python:3.7-alpine

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN echo http://mirrors.ustc.edu.cn/alpine/v3.9/main > /etc/apk/repositories
RUN echo http://mirrors.ustc.edu.cn/alpine/v3.9/community >> /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add mysql
RUN apk add make
RUN pip install --upgrade pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple/

# Application
WORKDIR /app
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY blog blog
COPY migrations migrations
COPY start_server.sh start_server.sh
#COPY wsgi.py wsgi.py
COPY Makefile Makefile

RUN pipenv install --deploy --system
RUN chmod a+x start_server.sh

EXPOSE 5000
ENTRYPOINT [ "./start_server.sh" ]
