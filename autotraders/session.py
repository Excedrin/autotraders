from typing import Optional

import requests
from pyrate_limiter import Limiter, RequestRate, Duration
from requests_ratelimiter import LimiterSession


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class AutoTradersSession(LimiterSession):
    def __init__(self, base_url="https://api.spacetraders.io/v2/"):
        super().__init__(per_second=2, burst_rate=10, limit_statuses=[429, 502])
        self.base_url = base_url
        self.headers.update({"Prefer": "dynamic=true"})


def get_session(token: Optional[str]) -> AutoTradersSession:
    """Creates a session with the provided token."""
    s = AutoTradersSession()
    if token is not None:
        s.auth = BearerAuth(token)
    return s
