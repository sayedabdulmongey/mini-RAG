from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from time import time


COUNT_REQUEST = Counter('http_requests_total', 'Total HTTP requests', [
                        'method', 'endpoint', 'status'])
LATENCY_REQUEST = Histogram('http_request_duration_seconds', 'Request duration', [
                            'method', 'endpoint', 'status'])


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        start_time = time()

        response = await call_next(request)

        duration = time() - start_time

        method = request.method
        endpoint = request.url.path
        status_code = response.status_code

        COUNT_REQUEST.labels(
            method=method, endpoint=endpoint, status=status_code).inc()
        LATENCY_REQUEST.labels(
            method=method, endpoint=endpoint, status=status_code).observe(duration)

        return response


def setup_metrics(app: FastAPI):

    app.add_middleware(PrometheusMiddleware)

    @app.get('/Qw8rT2k9_LmN7zX4vB1cA7eP5sR3hJ2k', include_in_schema=False)
    def metrices():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
