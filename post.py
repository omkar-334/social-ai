import asyncio
from datetime import datetime


class Post:
    def __init__(self, author, content):
        self.id = f"{author} - {content[:25]}"
        self.author = author
        self.content = content
        self.replies = []
        self.timestamp = datetime.now()
        self.lock = asyncio.Lock()

    async def reply(self, user, reply):
        async with self.lock:
            self.replies.append((datetime.now(), user, reply))

    def construct_reply_history(self):
        history = ""
        if self.replies:
            for reply in self.replies:
                history += (
                    f"Time - {reply.timestamp}; "
                    + f"User - {reply.author}; "
                    + f"Reply - {reply.content}\n"
                )

        return history


class Reply:
    def __init__(self, author, content, postid):
        self.author = author
        self.content = content
        self.timestamp = datetime.now()
        self.postid = postid
