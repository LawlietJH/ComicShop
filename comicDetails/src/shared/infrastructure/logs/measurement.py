class Measurement:
    """
    Class that allows us to obtain traceability by transaction within the
    service logs.
    """

    def __init__(self, service: str, time: int | float,
                 message: str = 'Success'):
        self.service = service
        self.message = message
        self.time_elapsed = time

    def get_service(self):
        return {
            'service': self.service,
            'message': self.message,
            'time_elapsed': self.time_elapsed
        }
