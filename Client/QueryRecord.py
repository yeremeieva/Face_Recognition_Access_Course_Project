import requests

url = "http://localhost:8090"

def person_record(student_id, start_time, end_time):
    res = {
        "student_id": student_id,
        "start_time": start_time,
        "end_time": end_time,
    }
    returnData = requests.post(f"{url}/person_record", json=res)
    return returnData.text


def door_record(self, door_id, direction, start_time, end_time):
    res = {
        "door_id": door_id,
        "direction": direction,
        "start_time": start_time,
        "end_time": end_time,
    }
    returnData = requests.post(f"{self.url}/door_record", json=res)
    return returnData.text

