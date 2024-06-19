import logging

from yadisk import YaDisk


class DiskClass:
    def __init__(self, token):
        self.token = token
    async def disk_check_token(self):
        disk = YaDisk(token=self.token)

        return disk.check_token()
