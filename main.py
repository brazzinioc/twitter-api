import uvicorn
import json
from typing import List

from config import APP_NAME, HOST, PORT, DEBUG

from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from passlib.context import CryptContext

# models
from models import User, UserIn, UserOut, UserRegister
from models import Tweet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI(title=APP_NAME)


# Path Operations

## User

### Register a User
@app.post(
    path="/singup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"],
)
def singup(user: UserRegister = Body(...)):
    """
    **SINGUP**

    This path operation register a User in the app.

    **Parameters:**  
        - Request body parameter  
        - user: UserRegister  
        
    **Return:**  
    A json with the basic user information.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime
    """

    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios

        user_dict = user.dict()  # crea un nuevo diccionario
        user_dict["id"] = str(user_dict["id"])  # cambia el id a str 
        user_dict["born_date"] = str(user_dict["born_date"])
        user_dict["created_at"] = str(user_dict["created_at"]) 
        user_dict["updated_at"] = str(user_dict["updated_at"]) 
        user_dict["deleted_at"] = str(user_dict["deleted_at"]) 
        results.append(user_dict)

        f.seek(0)  # posiciona el cursor al inicio del archivo
        f.write(json.dumps(results))  # escribe el json en la posicion del cursor

        return user


### Login a User
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"],
)
def login():
    pass


### Show all Users
@app.get(
    path="/users",
    response_model=List[User],  # formato lista -> json
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"],
)
def show_all_users():
    """
    Show Users

    This path operation show all users in the app.

    Parameters:
      -

    Returns a json list with all Users.
      - id: UUID
      - email: Emailstr
      - first_name: str
      - last_name: str
      - birthday: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios

        return results


### Show a User
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"],
)
def show_a_user():
    pass


### Update a User
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"],
)
def update_a_user():
    pass


### Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"],
)
def delete_a_user():
    pass


## Tweets

### Show all Tweets
'''
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"],
)
def show_all_tweets() -> List[Tweet]:
    """
    Show Tweets

    This path operation show all Tweets in the app.

    Parameters:
      -

    Returns a json list with all Users.
      - id: UUID
      - content: str
      - created_at: datetime
      - updated_at: Optional[datetime]
      - created_by: user
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios

        return results


### Register a Tweet
@app.post(
    path="/tweets",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Register a Tweet",
    tags=["Tweets"],
)
def create_a_tweet(tweet: Tweet = Body(...)):
    """
    Create a Tweet

    This path operation create a Tweet in the app.

    Parameters:
      - Request body parameter
        - tweet: Tweet

    Returns a json with the basic tweet information.

      - id: UUID
      - content: str
      - created_at: datetime
      - updated_at: Optional[datetime]
      - created_by: User
    """

    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios

        tweet_dict = tweet.dict()  # crea un nuevo diccionario
        tweet_dict["id"] = str(tweet_dict["id"])  # convierte el id a string
        tweet_dict["created_at"] = str(
            tweet_dict["created_at"]
        )  # convierte la fecha a string

        # cast User data. Without this cast the app show an error
        tweet_dict["created_by"]["id"] = str(
            tweet_dict["created_by"]["id"]
        )  # convierte el id a string
        tweet_dict["created_by"]["birthday"] = str(
            tweet_dict["created_by"]["birthday"]
        )  # convierte la fecha a string

        if tweet_dict["updated_at"] is not None:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])

        results.append(tweet_dict)

        f.seek(0)  # posiciona el cursor al inicio del archivo
        f.write(json.dumps(results))  # escribe el json en la posicion del cursor

        return tweet


### Show a Tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"],
)
def show_a_tweet():
    pass


### Update a Tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"],
)
def update_a_tweet():
    pass


### Delete a Tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"],
)
def delete_a_tweet():
    pass
'''

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=str(HOST),
        port=int(PORT),
        workers=2,
        log_level="info",
        reload=True,
        debug=bool(DEBUG),
    )
    print("Starting server...")
