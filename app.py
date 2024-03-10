from fastapi import FastAPI, Response
import random

app = FastAPI()

@app.get("/", status_code=200)
async def root(num: int, response: Response):
    # rand_num = random.randint(0, 10)
    # if rand_num % 2 == 0:
    if num == 4 or num == 14 or num == 44 or num ==69:
        response.status_code = 500
        return {"error": True}
    else: 
        return {"message": f"hello world--you printed {num}", "data": num * 2, "math": [num * 3, num * 4]}
     