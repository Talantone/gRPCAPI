async def on_send_request(event: SendRequest) -> None:
    request_id = event.metadata['x-request-id'] = str(uuid.uuid4())
    print(f'Generated Request ID: {request_id}')

