from datetime import datetime
import uvicorn
import json
from typing import List
from uuid import UUID
import os

from config import APP_NAME, HOST, PORT, DEBUG

from fastapi import FastAPI, status, Body, Form, Path, HTTPException
from passlib.context import CryptContext

# models
from models import User, UserIn, UserOut
from models import Tweet

# for password hash and verify
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
def singup(user: UserIn = Body(...)):
    """
    **SINGUP**
    This path operation register a User in the app.

    **Parameters:**  
        - Request body parameter  
        - user: UserIn  
        
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
    print("current path")
    print(os.getcwd())
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios

        user_dict = user.dict()  # crea un nuevo diccionario
        user_dict["id"] = str(user_dict["id"])  # cambia el id a str 
        user_dict["password"] = pwd_context.hash(user_dict['password'])
        user_dict["born_date"] = str(user_dict["born_date"])
        user_dict["created_at"] = str(user_dict["created_at"]) 
        results.append(user_dict)

        f.seek(0)  # posiciona el cursor al inicio del archivo
        f.write(json.dumps(results))  # escribe el json en la posicion del cursor

        return user


### Login a User
@app.post(
    path="/login",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"],
)
def login(
    email: str = Form(
        ...,
        title="Email",
        description="User email"
        ),
    password: str = Form(
        ...,
        min_length=8,
        title="Password",
        description=""
        ),
    ):
    """
    **LOGIN**
    This path operation login a User in the app.

    **Parameters:**  
        - Request form parameter (email and password).

    **Return:**  
    If autentication is CORRECT return a json with the basic user information.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime  
    
    If autentication is INCORRECT return a message.  
        - **message:** str
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios
        
        if len(results) > 0:
            for user in results:
                if user["deleted_at"] is None and user["email"] == email:
                    if pwd_context.verify(password, user["password"]):
                        return User(id=user["id"], email=user['email'], first_name=user["first_name"], last_name=user["last_name"], born_date=user["born_date"], created_at=user["created_at"], updated_at=user["updated_at"], deleted_at=user["deleted_at"])

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email and Password are incorrects",
            headers={ "X-Error": "Email and Password are incorrects." }
        )



### Show all Users
@app.get(
    path="/users",
    response_model=List[UserOut],  # formato lista -> json
    status_code=status.HTTP_200_OK,
    summary="Show all Users",
    tags=["Users"],
)
def show_all_users():
    """
    **SHOW USERS**  
    This path operation show all users in the app.  
    
    **Parameters:**  
        - 
        
    **Return:**  
    A json list with all Users.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime  

    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())  # lista de diccionarios
        users = [] # Only User where deleted_at is None

        if len(results) > 0:
            for user in results:
                if user["deleted_at"] is None:
                    users.append(user)

        return users


### Show a User
@app.get(
    path="/users/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"],
)
def show_a_user(user_id: UUID = Path(...)):
    """
    **SHOW A USER**  
    This path operation show a active user in the app.  
    
    **Parameters:**  
        - Path parameter
        - user_id: uuid
        
    **Return:**  
    A json with User information.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime  
    """
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())  # lista de diccionarios
        
        if len(users) > 0:
            for u in users:
                if u["id"] == str(user_id) and u["deleted_at"] is None:
                    return UserOut(id=u["id"], email=u['email'], first_name=u["first_name"], last_name=u["last_name"], born_date=u["born_date"], created_at=u["created_at"], updated_at=u["updated_at"], deleted_at=u["deleted_at"])
    
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"X-Error": "User not found"}
        )


### Update a User
@app.put(
    path="/users/{user_id}/update",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"],
)
def update_a_user(
    user_id: UUID = Path(...),
    user: User = Body(...)
    ):
    """
    **UPDATE A USER**  
    This path operation update a active user in the app.  
    
    **Parameters:**  
        - Path parameter and Request Body
        - user_id: uuid  
        - user: User
        
    **Return:**  
    A json with User information.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime  
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        users = json.loads(f.read())  # lista de diccionarios
        
        if len(users) > 0:
            for i,u in enumerate(users):
                if u["id"] == str(user_id) and u["deleted_at"] is None:
                    user_dict = user.dict()
                    users[i]["email"] = user_dict["email"]
                    users[i]["first_name"] = user_dict["first_name"]
                    users[i]["last_name"] = user_dict["last_name"]
                    users[i]["born_date"] = str(user_dict["born_date"])
                    users[i]["created_at"] = str(user_dict["created_at"])
                    users[i]["updated_at"] = str(datetime.now())
                    
                    f.seek(0)  # posiciona el cursor al inicio del archivo
                    f.write(json.dumps(users))  # escribe el json en la posicion del cursor
                    f.close()

                    return UserOut(id=users[i]["id"], 
                                    email=users[i]['email'], 
                                    first_name=users[i]["first_name"], 
                                    last_name=users[i]["last_name"], 
                                    born_date=users[i]["born_date"], 
                                    created_at=users[i]["created_at"], 
                                    updated_at=users[i]["updated_at"], 
                                    deleted_at=users[i]["deleted_at"]
                                )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"X-Error": "User not found"}
        )



### Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"],
)
def delete_a_user(user_id: UUID = Path(...)):
    """
    **DELETE A USER**  
    This path operation delete a active user in the app.  
    
    **Parameters:**  
        - Path parameter
        - user_id: uuid
        
    **Return:**  
    A json with User information.  
        - **id:** uuid  
        - **email:** Emailstr  
        - **first_name:** str  
        - **last_name:** str  
        - **born_date:** datetime  
        - **created_at:** datetime  
        - **updated_at:** datetime  
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        users = json.loads(f.read())  # lista de diccionarios
        
        if len(users) > 0:
            for i,u in enumerate(users):
                if u["id"] == str(user_id) and u["deleted_at"] is None:
                    users[i]["deleted_at"] = str(datetime.now())
                    f.seek(0)  # posiciona el cursor al inicio del archivo
                    f.write(json.dumps(users))  # escribe el json en la posicion del cursor
                    f.close()

                    return UserOut(id=users[i]["id"], 
                                    email=users[i]['email'], 
                                    first_name=users[i]["first_name"], 
                                    last_name=users[i]["last_name"], 
                                    born_date=users[i]["born_date"], 
                                    created_at=users[i]["created_at"], 
                                    updated_at=users[i]["updated_at"], 
                                    deleted_at=users[i]["deleted_at"]
                                )


    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
        headers={"X-Error": "User not found"}
    )




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
'''
