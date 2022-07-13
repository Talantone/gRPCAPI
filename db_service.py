import datetime

from grpclib.server import Stream

from models import box
from protobufs import db_grpc, db_pb2
from protobufs.db_pb2 import CreateBoxRequest, CreateBoxResponse, GetBoxResponse, GetBoxRequest, GetBoxesResponse, \
    GetAllBoxesRequest, UpdateBoxResponse, UpdateBoxRequest, DeleteBoxRequest, DeleteBoxResponse, \
    GetBoxesInCategoryRequest, GetBoxesInTimeRangeRequest
from repository import boxes
from grpclib.events import RecvRequest
from google.protobuf.timestamp_pb2 import Timestamp




class DBService(db_grpc.DatabaseServiceBase):

    async def CreateBox(self, stream: Stream[CreateBoxRequest, CreateBoxResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None

        new_box = box.Box(
            name=request.box.name,
            price=request.box.price,
            description=request.box.description,
            category=request.box.category,
            quantity=request.box.quantity,
            created_at=datetime.datetime.utcnow()
        )

        response = await boxes.create_box(new_box)
        if response:
            message = db_pb2.RequestStatus.OK
        else:
            message = db_pb2.RequestStatus.ERROR

        await stream.send_message(CreateBoxResponse(status=message))

    async def GetBox(self, stream: Stream[GetBoxRequest, GetBoxResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        id = request.box.id
        box = await boxes.get_box_by_id(id)
        timestamp = Timestamp()
        time_response = timestamp.FromDatetime(box.created_at)

        message = db_pb2.Box(
            name=box.name,
            id=box.id,
            price=box.price,
            description=box.description,
            category=box.category,
            quantity=box.quantity,
            created_at=time_response
        )

        await stream.send_message(GetBoxResponse(box=message, status=db_pb2.RequestStatus.OK))

    async def GetBoxes(self, stream: [GetAllBoxesRequest, GetBoxesResponse]) -> None:
         response = await boxes.get_all_boxes()
         timestamp = Timestamp()
         message = []
         for box in response:
             time_response = timestamp.FromDatetime(box.created_at)

             message.append(db_pb2.Box(
                 name=box.name,
                 id=box.id,
                 price=box.price,
                 description=box.description,
                 category=box.category,
                 quantity=box.quantity,
                 created_at=time_response
             ))

         if response:
             status = db_pb2.RequestStatus.OK
         else:
             status = db_pb2.RequestStatus.ERROR

         await stream.send_message(GetBoxesResponse(box=message, status=status))

    async def UpdateBox(self, stream: Stream[UpdateBoxRequest, UpdateBoxResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        id = request.box.id

        update_box = box.UpdateBoxModel(
            name=request.box.name,
            price=request.box.price,
            description=request.box.description,
            category=request.box.category,
            quantity=request.box.quantity,
        )
        values = {**update_box.dict()}

        response = await boxes.update_box(id, values)
        if response:
            status = db_pb2.RequestStatus.OK
        else:
            status = db_pb2.RequestStatus.ERROR

        await stream.send_message(UpdateBoxResponse(status=status))

    async def DeleteBox(self, stream: Stream[DeleteBoxRequest, DeleteBoxResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        id = request.box.id

        response = await boxes.delete_box(id)
        if response:
            status = db_pb2.RequestStatus.OK
        else:
            status = db_pb2.RequestStatus.ERROR

        await stream.send_message(UpdateBoxResponse(status=status))

    async def GetBoxesInCategory(self, stream: Stream[GetBoxesInCategoryRequest, GetBoxesResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        cat = request.category
        response = await boxes.get_boxes_in_category(cat)
        timestamp = Timestamp()
        message = []

        for box in response:
            time_response = timestamp.FromDatetime(box.created_at)
            message.append(db_pb2.Box(
                name=box.name,
                id=box.id,
                price=box.price,
                description=box.description,
                category=box.category,
                quantity=box.quantity,
                created_at=time_response
            ))

        status = db_pb2.RequestStatus.OK

        await stream.send_message(GetBoxesResponse(box=message, status=status))

    async def GetBoxesInTimeRange(self, stream: Stream[GetBoxesInTimeRangeRequest, GetBoxesResponse]) -> None:
        request = await stream.recv_message()
        assert request is not None
        time1 = request.start_time.ToDatetime()
        time2 = request.end_time.ToDatetime()
        response = await boxes.get_boxes_in_time_range(time1, time2)
        timestamp = Timestamp()
        message = []

        for box in response:
            time_response = timestamp.FromDatetime(box.created_at)
            message.append(db_pb2.Box(
                name=box.name,
                id=box.id,
                price=box.price,
                description=box.description,
                category=box.category,
                quantity=box.quantity,
                created_at=time_response
            ))

        status = db_pb2.RequestStatus.OK

        await stream.send_message(GetBoxesResponse(box=message, status=status))
