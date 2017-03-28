import os

import aiofiles


class null:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass


class tmp_dl:
    def __init__(self, url, session, encoding='utf8'):
        self.url = url
        self.session = session
        self.encoding = encoding
        self.path = f'tmp/{self.url.rpartition('/')[-1]}'

    async def __aenter__(self):
        if not os.path.isdir('tmp'):
            os.mkdir('tmp')

        headers = {'Accept-Encoding': 'gzip, deflate, sdch',
                   }
        kwargs = {'timeout': None,
                  'headers': headers,
                  }

        async with aiofiles.open(self.path, 'wb') as file:
            async with self.session.get(self.url, **kwargs) as resp:
                async for block in resp.content.iter_any():
                    await file.write(block)
        self.file = await aiofiles.open(self.path, encoding=self.encoding)
        return self.file

    async def __aexit__(self, exc_type, exc, tb):
        try:
            os.remove(self.path)
            await self.file.close()
        except (FileNotFoundError, AttributeError):
            pass
