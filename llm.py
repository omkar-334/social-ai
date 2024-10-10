import random

from dotenv import load_dotenv

load_dotenv()


async def llm(system_prompt: str, user_prompt: str, args: dict) -> str:
    import os

    from groq import AsyncGroq

    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    chat_completion = await client.chat.completions.create(
        messages=messages,
        model=random.choice(models),
        stop=None,
        stream=False,
        **args,
    )

    return chat_completion.choices[0].message.content


models = [
    "gemma2-9b-it",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "mixtral-8x7b-32768",
]


def create_args(user, post=True):
    communication_style = user.communication_style
    engagement_level = user.engagement_level

    high_styles = ["sarcastic", "humorous", "provocative", "informal"]
    medium_styles = ["direct", "supportive", "empathetic", "formal"]
    low_styles = ["minimalist", "critical"]

    # SHould alter either temp or top_p (only one)

    if communication_style in high_styles:
        top_p = random.uniform(0.8, 0.95)
        temperature = random.uniform(0.7, 1.0)

    elif communication_style in medium_styles:
        top_p = random.uniform(0.6, 0.8)
        temperature = random.uniform(0.4, 0.7)

    elif communication_style in low_styles:
        top_p = random.uniform(0.3, 0.5)
        temperature = random.uniform(0.1, 0.4)

    if engagement_level == "active":
        top_k = random.randint(50, 100)
        max_tokens = random.randint(150, 200) if post else random.randint(50, 80)
        frequency_penalty = random.uniform(0.7, 1.0)
        presence_penalty = random.uniform(0.7, 1.0)
        temperature += 0.1

    elif engagement_level == "moderate":
        top_k = random.randint(20, 50)
        max_tokens = random.randint(80, 120) if post else random.randint(30, 60)
        frequency_penalty = random.uniform(0.4, 0.7)
        presence_penalty = random.uniform(0.4, 0.7)

    else:
        top_k = random.randint(5, 20)
        max_tokens = random.randint(40, 80) if post else random.randint(10, 40)
        frequency_penalty = random.uniform(0.1, 0.4)
        presence_penalty = random.uniform(0.1, 0.4)
        temperature -= 0.1

    return {
        "temperature": max(0.1, min(temperature, 1.0)),
        # "top_p": top_p,
        # "top_k": top_k,
        "max_tokens": max_tokens,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
    }


# def simulate_agents(agents, posts):
#     """Simulate agent decisions based on system and user prompts."""
#     for agent in agents:
#         system_prompt = f"System: What will {agent.username} do?"
#         print(system_prompt)

#         # The agent makes a decision based on their profile
#         action = agent.make_decision()

#         # User prompt gives feedback based on the action
#         user_prompt = f"{agent.username} has decided to: {action}"
#         print(user_prompt)

#         if action == "post":
#             content = f"Hello! This is a post from {agent.username}."
#             agent.post(content)
#             posts.append(agent.posts[-1])

#         elif action == "like" and posts:
#             post_to_like = random.choice(posts)
#             agent.like_post(post_to_like)

#         elif action == "reply" and posts:
#             post_to_reply = random.choice(posts)
#             reply_content = f"This is a reply from {agent.username}."
#             agent.reply_to_post(post_to_reply, reply_content)

#         elif action == "none":
#             print(f"{agent.username} chose not to engage at the moment.")

# C:\Users\omkar\Desktop\social\.venv\Lib\site-packages\strictjson\base_async.py
# async def post_agent(user, system_prompt, user_prompt):
#     result = await strict_json_async(
#         system_prompt=system_prompt,
#         user_prompt=user_prompt,
#         output_format={
#             "content": "The content of the post, type: str",
#             "tags": "The relevant tags/topics of the post, type: str",
#         },
#         llm=llm,
#         user=user,
#     )
#     return result


# async def reply_agent(user, system_prompt, user_prompt):
#     result = await strict_json_async(
#         system_prompt=system_prompt,
#         user_prompt=user_prompt,
#         output_format={
#             "reply": "The content of the reply (Return None if you choose not to reply), type: Union[str, None]",
#             # "thoughts": "The justification behind the reply, type: str",
#         },
#         llm=llm,
#         user=user,
#     )
#     return result
