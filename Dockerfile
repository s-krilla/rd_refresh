FROM python:alpine

ENV PUID=1000
ENV PGID=1000
ENV PUSER=rd_refresh
ENV PGROUP=rd_refresh

RUN mkdir -p /opt/rd

RUN addgroup -g $PGID $PGROUP && \
    adduser --shell /sbin/nologin --disabled-password \
    --home /opt/rd --uid $PUID --ingroup $PGROUP $PUSER

RUN pip install --no-cache-dir requests python-dotenv rd_api_py

RUN apk update && apk add --no-cache git

RUN git clone https://github.com/s-krilla/rd_refresh.git /opt/rd/refresh

RUN chmod +x /opt/rd/refresh/unrestrict.py && \
    chmod +x /opt/rd/refresh/refresh.py

RUN chown -R $PUSER:$PGROUP /opt/rd

USER $PUSER

WORKDIR /opt/rd/refresh

ENTRYPOINT [ "python" ]
CMD [ "refresh.py" ]
