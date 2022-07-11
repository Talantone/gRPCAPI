.PHONY: run


run:
	python3 main.py
proto:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpclib_python_out=. protobufs/db.proto

