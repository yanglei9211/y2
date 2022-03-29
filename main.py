import os
import traceback

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from controller.first import first_router
from model.mongodb import setup_mongodb_client, get_client
from setting import program_args
from controller.mapping import reflect_router
from util.escape import SafeJSONResponse
# from util.logger import init_logger
from util.errors import DTError
from util.logger import setup_logging, Logging

app = FastAPI()
app.include_router(first_router)
app.include_router(reflect_router)
# static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
# app.mount('/static', StaticFiles(directory=static_dir), name='static')


@app.exception_handler(DTError)
async def data_error_handler(request, exc):
    return SafeJSONResponse({'err_msg': exc})


@app.exception_handler(Exception)
async def system_exception_handler(request, exc):
    emsg = traceback.format_exc()
    exc = str(exc) + "\n" + emsg
    Logging.error(exc)
    return SafeJSONResponse({'err_msg': exc})


def start_server():
    host = '0.0.0.0'
    port = program_args.port
    setup_mongodb_client()
    setup_logging()
    # init_logger()
    uvicorn.run(app="main:app", host=host, port=port, reload=True, debug=True)


def close_server():
    pass


if __name__ == "__main__":
    start_server()
