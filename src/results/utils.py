from ansi2html import Ansi2HTMLConverter
from fastapi import Response

converter = Ansi2HTMLConverter()


async def create_response(stdout: bytes) -> Response:
    body = ""
    body += stdout.decode()
    print(body)
    convert_result = converter.convert(body).encode()
    response = Response(content=convert_result)
    response.headers["Content-Type"] = "text/html"
    response.headers["Content-Length"] = str(len(convert_result))

    return response
