from dataclasses import dataclass
from datetime import datetime
from typing import Any

from deep_translator import GoogleTranslator

from helpers import from_datetime, from_int, from_str, game_modes

traductor = GoogleTranslator(source="en", target="es")


@dataclass
class Event:
    id: int
    mode: str
    map: str

    @staticmethod
    def from_dict(obj: Any) -> "Event":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        mode = from_str(obj.get("mode"))
        mode = game_modes.get(mode, mode)
        map = from_str(obj.get("map"))
        map = traductor.translate(map)
        return Event(id, mode, map)


@dataclass
class Rotation:
    start_time: datetime
    end_time: datetime
    slot_id: int
    event: Event

    @staticmethod
    def from_dict(obj: Any) -> "Rotation":
        assert isinstance(obj, dict)
        start_time = from_datetime(obj.get("startTime"))
        end_time = from_datetime(obj.get("endTime"))
        slot_id = from_int(obj.get("slotId"))
        event = Event.from_dict(obj.get("event"))
        return Rotation(start_time, end_time, slot_id, event)
