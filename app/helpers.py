import json
from typing import List
from uuid import UUID


def verifyUser(id: UUID) -> bool:
    """
    Verify if the user exists.
    """
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())
        
        if len(users) > 0:
            for user in users:
                if user["id"] == str(id):
                    return True
    return False


# verify if users json file exists and if not create it
def verifyJsonDb(files: List[str]) -> bool:
    """
    Verify if json file exists and if not create it.
    """
    if len(files) > 0:
        for f in files:
            try:
                with open("{}.json".format(f), "r", encoding="utf-8") as f:
                    pass
            except FileNotFoundError:
                with open("{}.json".format(f), "w", encoding="utf-8") as f:
                    f.write("[]")
                    f.close()
