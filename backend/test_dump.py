from pydantic import BaseModel

class MyModel(BaseModel):
    data: str

def test_model_dump():
    # Scenario 1: Correct usage
    m = MyModel(data="hello")
    print(f"Model dump: {m.model_dump()}")

    # Scenario 2: The error we see
    s = "im a string"
    try:
        s.model_dump()
    except AttributeError as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    test_model_dump()
