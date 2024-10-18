import random

from colors import user_colors
from llm import clean, create_args, llm, models
from post import Post, Reply
from prompts import post_prompt, reply_prompt, system_prompt


class User:
    def __init__(self, name, bio="", interests=[], icon_url=None):
        self.name = name
        self.bio = bio
        self.interests = interests
        self.icon_url = icon_url
        self.color = random.choice(user_colors)
        self.model = random.choice(models)
        self.posts = []
        self.communication_style = random.choice(
            [
                "direct",
                "sarcastic",
                "formal",
                "informal",
                "humorous",
                "supportive",
                "critical",
                "provocative",
                "empathetic",
                "minimalist",
            ]
        )
        self.engagement_level = random.choice(["active", "moderate", "passive"])
        self.engagement_style = random.choice(["proactive", "reactive"])
        self.response_speed = random.choice(["instant", "delayed"])

    def construct_post_history(self):
        history = ""
        if self.posts:
            for post in self.posts:
                history += f"Time - {post.timestamp}; " + f"Post - {self.content}; "

        return history

    async def post(self, model=None):
        print(model)
        args = create_args(self, model, post=True)

        SYSTEM_PROMPT = system_prompt(self)
        USER_PROMPT = post_prompt(self, args["max_tokens"])

        response = await llm(SYSTEM_PROMPT, USER_PROMPT, args)
        post = Post(self, clean(response))
        return post

    async def reply(self, post, postid, model=None):
        args = create_args(self, model, post=False)

        SYSTEM_PROMPT = system_prompt(self)
        USER_PROMPT = reply_prompt(self, post, args["max_tokens"])

        response = await llm(SYSTEM_PROMPT, USER_PROMPT, args)
        reply = Reply(self, clean(response), postid)
        return reply

    def get_post_interval(self):
        # Engagement level affects how frequently users post
        if self.engagement_level == "active":
            return random.randint(5, 10)
        elif self.engagement_level == "moderate":
            return random.randint(7, 12)
        else:
            return random.randint(10, 15)
