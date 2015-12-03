import requests
import threading
from threading import Thread

class AsyncWebPageClient():
    lock_input = threading.Lock()
    lock_output = threading.Lock()
    count = 0
    position = 0
    result = []
    all_urls = []
    def __init__(self, n):
        for i in range(0, n):
            t = AsyncWebPageClient.ThreadLoad()
            t.start()
            self.count = 0

    class ThreadLoad(Thread):

        def run(self):
            while 1:
                # print self.all_urls

                AsyncWebPageClient.lock_input.acquire()
                if AsyncWebPageClient.position < len(AsyncWebPageClient.all_urls):
                    url = AsyncWebPageClient.all_urls[AsyncWebPageClient.position]
                    AsyncWebPageClient.position += 1
                    AsyncWebPageClient.lock_input.release()
                    try:
                        requests.get(url, hooks=dict(response=self.response_function))
                    except Exception as e:
                        AsyncWebPageClient.lock_output.acquire()
                        AsyncWebPageClient.result.append({'status_code': -1, 'err': e, 'url': url})
                        AsyncWebPageClient.count -= 1
                        AsyncWebPageClient.lock_output.release()
                else:
                    AsyncWebPageClient.lock_input.release()

        def response_function(self, r, *args, **kwargs):
            AsyncWebPageClient.lock_output.acquire()
            AsyncWebPageClient.result.append({'status_code': r.status_code, 'url': r.url, 'content': r.content})
            AsyncWebPageClient.count -= 1
            # print 'count = '+ str(AsyncWebPageClient.count)
            AsyncWebPageClient.lock_output.release()



    def get_pages(self, urls):
        AsyncWebPageClient.count = len(urls)
        AsyncWebPageClient.position = 0
        AsyncWebPageClient.lock_input.acquire()
        for url in urls:
            AsyncWebPageClient.all_urls.append(url)
        AsyncWebPageClient.lock_input.release()
        while AsyncWebPageClient.count > 1:
            pass

        return self.result
