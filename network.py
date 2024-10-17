import asyncio
import random

from colors import printpost, printreply


# TODO - Integrate both network functionalities
# Use this class for the terminal
class LoopNetwork:
    def __init__(self, users):
        self.users = users
        self.postsdict = {}

    async def simulate_network(self):
        tasks = [self.user_post_cycle(user) for user in self.users]
        await asyncio.gather(*tasks)

    async def user_post_cycle(self, user):
        while True:
            post_interval = user.get_post_interval()
            await asyncio.sleep(post_interval + 3)

            post = await user.post()
            if post.content:
                self.postsdict[post.id] = post
                printpost(post)

            reply_tasks = [
                self.user_reply_cycle(replying_user, post)
                for replying_user in self.users
                if replying_user != user
            ]
            await asyncio.gather(*reply_tasks)

    async def user_reply_cycle(self, user, post):
        reply = await user.reply(post)
        if reply.content:
            post.replies.append(reply)
            printreply(post, reply)


# Use this class for the gradio app
class AppNetwork:
    def __init__(self, users):
        self.users = {user.name: user for user in users}
        self.posts_dict = {}

    async def create_post(self, username=None):
        if not username:
            username = random.choice(list(self.users.keys()))
        user = self.users.get(username)

        if user:
            post = await user.post()
            if post.content:
                self.posts_dict[post.id] = post
                printpost(post)
                return post
        return None

    async def create_reply(self, post_id, username=None):
        if post_id in self.posts_dict:
            post = self.posts_dict[post_id]
            if not username:
                username = random.choice(list(self.users.keys()))
            user = self.users.get(username)
            if user:
                reply = await user.reply(post, post.id)
                if reply.content:
                    post.replies.append(reply)
                    printreply(post, reply)
                    return reply
        return None
