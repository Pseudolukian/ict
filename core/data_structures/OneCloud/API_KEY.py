from pydantic import BaseModel, Field, validator
import os


class IncorrectApiKey(ValueError):
    def __str__(self):
        return "You are input incorrect API-key. Please, try again."

class API_key(BaseModel):
    API_key:str = Field(default = "")

    def __str__(self):
        os.environ['API_KEY'] = self.API_key
        return self.API_key

   
    @staticmethod
    def input_key():
        while True:
            value = input("Введите API-ключ (64 символа): ")
            if len(value) != 64:
                print("You are input incorrect API-key. Please, try again.")
            else:
                print("You are input correct API-key. Now you can use ict.")
                return value

    @validator("API_key", pre=True, always=True)
    def api_key_checker(cls, value):
        if not value:
            value = cls.input_key()
        if len(value) != 64:
            raise IncorrectApiKey
        return value