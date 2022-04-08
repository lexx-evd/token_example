# token_example

### requirements, если захочется воспроизвести
```
# python
$ python --version
Python 3.9.5
$ pip install protobuf
Requirement already satisfied: protobuf in ~/venv/lib/python3.9/site-packages (3.20.0)

# generate token_pb2, creative_pb2
$ protoc -I=proto --python_out=proto proto/creative.proto proto/token.proto
# protoc скачать бинарем или собрать из исходников https://github.com/protocolbuffers/protobuf/releases/tag/v3.20.0
```
