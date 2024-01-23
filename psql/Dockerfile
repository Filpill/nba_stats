FROM postgres:13

WORKDIR /app

COPY tf tf
COPY etl.sh etl.sh

ENTRYPOINT [ "bash" ]

RUN chmod +x etl.sh

CMD [ "./etl.sh" ]
