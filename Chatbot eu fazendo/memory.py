from langchain_community.chat_message_histories import RedisChatMessageHistory

import redis

from config import REDIS_URL

def get_redis_memory(session_id):
    return RedisChatMessageHistory(
        session_id=session_id,
        url = REDIS_URL
    )