import time
class BrowserCache:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance  

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            self.cache = {}
            self._initialized = True



    def checkCachable(self, cache_control: str):
        time_to_cache = 0.0
        if cache_control.count("no-store"):
            self.isCachable = False
        elif cache_control.count("max-age"):
            time_to_cache = float(cache_control.split("=")[1])
            print(time_to_cache)
        self.isCachable = True
        return time_to_cache
    
    def memoize(self, f, *args):
        if args in self.cache:
            entry = self.cache[args]
            print(entry)
            if(entry["time_to_live"] != 0 and time.time() > entry["start_time"] + entry["time_to_live"]):
                result, view_source, _ = f(*args)
                self.cache[args] = {"result": result, "view_source": view_source, "time_to_live": entry["time_to_live"], "start_time": time.time()}
            return self.cache[args]["result"], self.cache[args]["view_source"], ""
        else:
            result, view_source, cache_control = f(*args)
            caching_time = self.checkCachable(cache_control)
            if self.isCachable:
                self.cache[args] = {"result": result, "view_source": view_source, "time_to_live": caching_time, "start_time": time.time()}
                print("Cachable and cache is: ")
                print(self.cache)
            return result, view_source, cache_control 
