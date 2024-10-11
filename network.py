import asyncio

from colors import printpost, printreply


# TODO - Integrate both network functionalities
# Use this class for the terminal
class Network:
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
        self.users = users
        self.posts_dict = {}
        self.running = True

    async def start(self):
        while self.running:
            for user in self.users:
                post_interval = user.get_post_interval()
                await asyncio.sleep(post_interval)
                if not self.running:
                    break

                post = await user.post()
                if post.content:
                    self.posts_dict[post.id] = post
                    printpost(post)
                    yield post

                for replying_user in self.users:
                    if replying_user != user:
                        reply = await replying_user.reply(post, post.id)
                        if reply.content:
                            post.replies.append(reply)
                            printreply(post, reply)
                            yield reply

    async def stop(self):
        self.running = False
