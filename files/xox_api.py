import json
from .tic_graph import bot


def xox_api(request):
    data = json.loads(request)

    move = bot(
        data["board"],
        data["player"],
        data.get("level", 2)
    )

    return json.dumps({"move": move})