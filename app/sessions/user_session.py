from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    """
    Rate limiter to restrict the number of requests made by a user within a specific time frame.
    Args:
        None
    Attributes:
        requests (dict): A dictionary to store the request count and reset time for each user.
        lock (asyncio.Lock): A lock to ensure thread-safe access to the requests dictionary.
    """
    def __init__(self):
        self.requests = {}
        self.lock = asyncio.Lock()

    async def is_allowed(self, user_id):
        async with self.lock:
            current_time = datetime.now()
            record = self.requests.get(user_id, {'count': 0, 'reset_time': current_time + timedelta(hours=1)})

            if current_time >= record['reset_time']:
                # Reset the record if the current time is past the reset time
                record = {'count': 0, 'reset_time': current_time + timedelta(hours=1)}

            if record['count'] >= 30:
                return False  # Block the user for this hour

            # Increment the request count
            record['count'] += 1
            self.requests[user_id] = record
            return True