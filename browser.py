from URL import URL
import time
def show(body, view_source):
    in_tag = False
    i = 0
    if view_source:
        print(body)
        return
    while i < len(body):
        c = body[i]
        if body[i:i+4] == "&lt;":
            print("<", end="")
            i += 3
        elif body[i:i+4] == "&gt;":
            print(">", end="")
            i += 3
        elif c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
        i += 1

def load(url, httpVersion = "1.1", browser = "Chrome"):
    body, view_source, _ = url.request(httpVersion, browser)
    show(body, view_source)    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        start_time = time.time()
        load(URL())
        first_time = time.time()
        load(URL())
        cached_time = time.time()

    elif len(sys.argv) == 2:
        start_time = time.time()
        load(URL(sys.argv[1]))
        first_time = time.time()
        load(URL(sys.argv[1]))
        cached_time = time.time()


    else:
        load(URL(sys.argv[1]), sys.argv[2], sys.argv[3])
        load(URL(sys.argv[1]))
        
    print("Normal time: ", first_time - start_time)
    print("Cached time: ", cached_time - first_time)