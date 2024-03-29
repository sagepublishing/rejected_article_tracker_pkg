
class FakeElapsedTime:
    def __init__(self, time):
        self.time = time

    def total_seconds(self):
        return self.time


class FakeResponse:

    def __init__(self, elapsed):
        self.elapsed = elapsed
        self.status_code = 200

    def json(self):
        return {
            'message': {
                'items': [
                    {'DOI':"Article #1"},
                    {'DOI':"Article #2"},
                    {'DOI':"Article #3"},
                ]
            }
        }


def get(address, params, headers):
    seconds = 1.0 if params['query.bibliographic'] != 'DELAYED' else 11
    elapsed = FakeElapsedTime(seconds)
    return FakeResponse(elapsed=elapsed)

