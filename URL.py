import socket
import ssl
import gzip
from BrowserCache import BrowserCache
class URL:
    def __init__(self, url = ""):
        self.fullUrl = url
        self.cache = BrowserCache()
        self.cache_control = ""
        self.count_redirects = 0
        self.view_source = False
        if url == "":
            self.scheme = "file"
            self.path = "test.html"
            return
        
        self.scheme, url = url.split(":", 1)
        if self.scheme == "view-source":
            self.view_source = True
            self.scheme, url = url.split(":", 1)
        url = url.removeprefix("//")
        assert self.scheme in ["http", "https", "file", "data"]
        match self.scheme:
            case "data":
                _, self.content = url.split(",", 1)
                return
            case "file":
                _, self.path = url.split("/", 1)
                return
            case "http":
                self.port = 80
            case "https":
                self.port = 443
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self, httpVersion = "", browser = ""):
        return self.cache.memoize(self.request_helper, httpVersion, browser, self.fullUrl)
    
    def request_helper(self, httpVersion = "", browser = "", fullUrl = ""):
        match self.scheme:
            case "data":
                return self.content, self.view_source, ""
            case "file":
                f = open(self.path)
                return f.read(), self.view_source, ""
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        s.connect((self.host, self.port))
        
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        request = ""
        
        if httpVersion == "1.0":
            request = "GET {} HTTP/1.0\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "Accept-Encoding: {}\r\n".format("gzip")
        elif httpVersion == "1.1":
            request = "GET {} HTTP/1.1\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "Connection: close\r\n"
            request += "User-Agent: {}\r\n".format(browser)
            request += "Accept-Encoding: {}\r\n".format("gzip")

        request += "\r\n"
        s.send(request.encode("utf8"))
        response = s.makefile("rb", newline="\r\n")
        statusline = response.readline()
        statusline = statusline.decode("utf-8")
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        
        while True:
            line = response.readline()
            line = line.decode('utf-8')
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        if int(status) >= 300 and int(status) < 400 and "location" in response_headers:
            location: str = response_headers.get("location")
            if(location.count(self.host) < 0):
                location += self.host
            if(location.count(self.scheme) < 0):
                location += self.scheme
            self.url = location
            if self.count_redirects > 50:
                return "", self.view_source
            self.count_redirects += 1
            return self.request(httpVersion, browser)
        
        # assert "transfer-encoding" not in response_headers
        print(response_headers)
        if "content-encoding" in response_headers:
            content = response.read()
            print(content)
            content = gzip.decompress(content)
            content = content.decode('utf-8')
        if "cache-control" in response_headers:
            self.cache_control = response_headers["cache-control"]
        return content, self.view_source, self.cache_control

