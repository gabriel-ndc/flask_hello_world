import uuid
import random
from typing import Any

from flask import Flask, request_started, request
import structlog

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.dict_tracebacks,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer()
    ]
)
log = structlog.get_logger()

def bind_request_details(sender: Flask, **extras: dict[str, Any]) -> None:
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=str(uuid.uuid4())   
    )

app = Flask(__name__)
request_started.connect(bind_request_details, app)


@app.route("/")
def index():
    log.info("Request for index")
    return app.json.response("Hello world!")


@app.route("/echo")
def echo():
    args = request.args
    message = args.get("message", "...silence")

    log.info("Message: %s", message)
    return {"message": message}


@app.route("/bad-request")
def bad_request():
    log.info("Should return 400...")
    return {"message": "Bad Request"}, 400


@app.route("/random-server-error")
def random_server_error():
    log.info("Should return 500 sometimes")
    random_number = random.randint(1,3)
    if random_number == 1:
        return {"message": "Oops"}, 500
    else:
        return {"message": "Alright"}


if __name__ == "__main__":
    app.run(port=5001, debug=True)