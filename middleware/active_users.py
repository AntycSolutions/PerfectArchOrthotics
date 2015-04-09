import time


class ActiveUserMiddleware():

    def process_request(self, request):
        # session variables must be serializable, can't use datetime
        cur_time = int(time.time())

        request.session['last_logged_in'] = cur_time
