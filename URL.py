import socket
import ssl

class URL:
    def __init__(self, url = ""):
        if url == "":
            self.scheme = "file"
            self.path = "test.html"
            return
        
        self.scheme, url = url.split(":", 1)
        if self.scheme[:2] == "//":
            _, self.scheme = self.scheme.split("//", 1)
        assert self.scheme in ["http", "https", "file", "data"]
        match self.scheme:
            case "data":
                _, self.content = url.split(",", 1)
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
        match self.scheme:
            case "data":
                return content
            case "file":
                f = open(self.path)
                return f.read()
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
        elif httpVersion == "1.1":
            request = "GET {} HTTP/1.1\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "Connection: close\r\n"
            request += "User-Agent: {}\r\n".format(browser)
        request += "\r\n"

        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        s.close()
        return content

