import redis
from config import Config

db = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

def user_timeout(user_ip, song_length):
    user_ip = "cdr_" + user_ip
    queue_length = db.get(user_ip)
    if queue_length != None:
        queue_length = int(queue_length)
        if queue_length < Config.ALLOWED_QUEUE:
            new_queue_length = queue_length + song_length
            if new_queue_length < Config.ALLOWED_QUEUE:
                db.setex(user_ip, Config.DEFAULT_EXPIRE, new_queue_length)
            else:
                new_expire = int(calculate_timeout(new_queue_length))
                db.setex(user_ip, new_expire, new_queue_length)
    else:
        if song_length < Config.ALLOWED_QUEUE:
            db.setex(user_ip, Config.DEFAULT_EXPIRE, song_length)
        else:
            new_expire = calculate_timeout(song_length)
            db.setex(user_ip, new_expire, song_length)

def calculate_timeout(queue_length):
    # Do the calculation here.
    queue_remainder = queue_length - (Config.ALLOWED_QUEUE)
    if queue_remainder < 0:
        new_expire = Config.DEFAULT_TIMEOUT
        return new_expire
    else:
        new_expire = (int(queue_remainder/60) * 15) + Config.DEFAULT_TIMEOUT
        return new_expire
		
def user_allowed(user_ip):
    user_ip = "cdr_" + user_ip
    queue_length = db.get(user_ip)
    if queue_length == None:
        return True
    elif int(float(queue_length)) < Config.ALLOWED_QUEUE:
        return True
    else:
        return False