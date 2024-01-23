FROM python:3.11

RUN pip install pgcli

WORKDIR /app

COPY query query
COPY login.sh login.sh

ENTRYPOINT [ "bash" ]

RUN chmod +x login.sh

CMD [ "./login.sh" ]