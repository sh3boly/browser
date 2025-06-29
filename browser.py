from URL import URL

def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url, httpVersion = "1.1", browser = "Chrome"):
    body = url.request(httpVersion, browser)
    show(body)    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        load(URL())
    elif len(sys.argv) == 2:
        load(URL(sys.argv[1]))
    else:
        load(URL(sys.argv[1]), sys.argv[2], sys.argv[3])