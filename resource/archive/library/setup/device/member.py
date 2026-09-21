from library.setup.device.ad_server import ADServer


class MemberServer(ADServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)