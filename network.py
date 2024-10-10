import asyncio

from colors import printpost, printreply


class Network:
    def __init__(self, users):
        self.users = users
        self.posts = []
        self.postsdict = {}

    async def simulate_network(self):
        tasks = [self.user_post_cycle(user) for user in self.users]
        await asyncio.gather(*tasks)

    async def user_post_cycle(self, user):
        while True:
            post_interval = user.get_post_interval()
            await asyncio.sleep(post_interval + 3)

            post = await user.post()
            if post:
                self.posts.append(post)
                self.postsdict[post.id] = post
                printpost(user, post)

            reply_tasks = [
                self.user_reply_cycle(replying_user, post)
                for replying_user in self.users
                if replying_user != user
            ]
            await asyncio.gather(*reply_tasks)

    async def user_reply_cycle(self, user, post):
        reply = await user.reply(post)
        if reply:
            post.replies.append(reply)
            printreply(user, post, reply)
