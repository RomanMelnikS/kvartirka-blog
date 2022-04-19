FROM python:3.9
WORKDIR /code
COPY . .
RUN chmod +x ./start.sh
CMD ["./start.sh"]