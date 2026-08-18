import json
import datetime

def write_log(ticket_id, step_name):

    log_file = f"logs/{ticket_id}.json"

    entry = {
        "step": step_name,
        "timestamp": str(datetime.datetime.now())
    }

    try:
        with open(log_file, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(log_file, "w") as f:
        json.dump(data, f, indent=4)