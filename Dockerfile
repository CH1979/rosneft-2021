FROM python:3.8.11-slim-buster

COPY ./ /app/

RUN pip install --no-cache-dir --requirement /app/requirements.txt && \
    rm --force --recursive /var/lib/apt/lists/* && \
    rm --force --recursive /tmp/*

WORKDIR /app/src

ENTRYPOINT ["python", "-m", "design_data_extraction"]

CMD ["--mode=predict", "--data-dir=/data", "--output-dir=/result"]
