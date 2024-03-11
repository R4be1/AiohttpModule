# AiohttpModule
## How to call the Module? So easy!
```shell
git clone https://github.com/R4be1/AiohttpModule.git
```

```python3
from AiohttpModule.aiocore import requests_responses
tasks = [
        {'webroot' : 'http://www.example.com', 'path' : '/index.html'},
        {'webroot' : 'http://www.example.com', 'path' : '/bak'},
        {'webroot' : 'http://www.example.com', 'path' : '/404'}
        ]
requests_responses( tasks )
# return [ { "url" : str(), "status_code" : int(), "text-length" : int(), "headers" : dict(), "text" : str(), "content" : bytes() } ]
```