from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    tags=["General"]
)

@router.get("/", summary="root", description="Show status (always 'running' :D)")
def root():
    return {"status": "running"}


@router.get("/hello", summary="greet", description="Greet user, default is 'guest'")
def hello(name="guest"):
    return {"message": f"Hello {name}!"}


@router.get("/square", summary="number^2", description="Return the square of the value")
def square(number: float):
    return {"number": number, "result": number**2}


@router.get("/multiply", summary="a * b", description="Multiply two numbers")
def multiply(a: float, b: float):
    return {"a": a, "b": b, "result": a * b}


@router.get("/divide", summary="a / b", description="Divide two numbers")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="b cannot be '0'"
        )
    return {"a": a, "b": b, "result": a / b}
