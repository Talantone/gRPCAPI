import datetime
from typing import List


from models.box import Box

box_collection = Box


async def create_box(box: Box) -> Box:
    new_box = await box_collection.insert(box)
    return new_box


async def get_box_by_id(id: int) -> Box:
    box = await box_collection.find_one(box_collection.id == id)
    if box:
        return box


async def get_all_boxes() -> List[Box]:
    boxes = await box_collection.all().to_list()
    return boxes


async def update_box(id: int, data: dict) -> bool:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    box = await box_collection.find_one(box_collection.id == id)
    if box:
        await box.update(update_query)
        return True
    return False


async def delete_box(id: int) -> bool:
    box = await box_collection.find_one(box_collection.id == id)
    if box:
        await box.delete()
        return True


async def get_boxes_in_category(cat: str) -> List[Box]:
    boxes = await box_collection.find(box_collection.category == cat).to_list()
    return boxes


async def get_boxes_in_time_range(time1: datetime.datetime, time2: datetime.datetime) -> List[Box]:
    boxes = await box_collection.find({"created_at": {"$gte": time1, "$lt": time2}}).to_list()
    return boxes
