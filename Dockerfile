FROM cryptokasten/cryptokasten-create-from-template-environment
RUN mkdir /code
COPY src/* /code
ENTRYPOINT ["python" "/code/cryptokasten_create_from_tempate.py"]
