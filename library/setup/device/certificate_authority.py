from library.setup.device.ad_server import ADServer


class CertificateAuthority(ADServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)