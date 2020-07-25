from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

url = 'https://cookpad.com/id/resep/13260747-roti-singkong-pakai-rebread'

result = PurePosixPath(
    unquote(
        urlparse(
            url
        ).path
    )
).parts[3]

print(result)