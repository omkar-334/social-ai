import asyncio

import gradio as gr

from llm import openai_models
from network import AppNetwork
from profiles import human, users

users = {user.name: user for user in users}
simulation = AppNetwork(users, human)


def format_message(item, is_reply=False):
    margin_left = "45px" if is_reply else "0"
    font_size = "12px" if is_reply else "16px"

    icon_html = (
        f'<img src="{item.author.icon_url}" style="width: 28px; height: 28px; border-radius: 50%; margin-right: 10px;">'
        if item.author.icon_url
        else ""
    )
    if not is_reply:
        copy_html = f"""
            <button onclick="navigator.clipboard.writeText('{item.id}')" style="margin-left: 5px; font-size: 12px; background-color: #f59e0b; color: black; border: none; border-radius: 4px; padding: 2px 6px; cursor: pointer;">Copy Post ID</button></p>
        """
    else:
        copy_html = ""

    message_html = f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 15px; margin-left: {margin_left}; background-color: #3d3b3b; border-radius: 8px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        {icon_html}
        <div style="display: flex; flex-direction: column; flex-grow: 1; width: 100%;">
                <p style="color: #ffffff ; font-size: {font_size}; margin: 0; font-weight: bold; line-height: 1;">{item.author.name}{copy_html}</p>
            <p style="margin: 8px 0 0 0; font-size: 14px; line-height: 1.4; color: #ffffff;">{item.content}</p>
        </div>
    </div>
    """
    return message_html


async def create_post(selected_user=None, human_text=None, model=None):
    if human_text:
        await simulation.create_post(human_text=human_text)
    else:
        await simulation.create_post(selected_user, model=model)
    return update_interface()


async def create_reply(post_id, selected_user=None, human_text=None, model=None):
    if human_text:
        await simulation.create_reply(post_id, human_text=human_text)
    else:
        if selected_user == "All Users":
            tasks = [
                simulation.create_reply(post_id, user_name, model=model)
                for user_name in users.keys()
            ]
            await asyncio.gather(*tasks)
        else:
            await simulation.create_reply(post_id, selected_user, model=model)
    return update_interface()


def update_interface():
    content = []

    for post in simulation.posts_dict.values():
        content.append(format_message(post))
        for reply in post.replies:
            content.append(format_message(reply, is_reply=True))

    htmlcontent = "".join(content)

    return f"""
        <div style="height: 600px; overflow-y: auto; padding: 10px; background-color: #1a1a1a; border-radius: 10px;">
            {htmlcontent}
        </div>
        """


with gr.Blocks(theme=gr.themes.Citrus()) as app:
    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown(
                "<h3>Social Network simulation</h3>"
                "<small>Copy the post ID to reply to a post<br>"
                + "Don't select user if you want to post or reply to a post youself, or if you want a random user.</small>"
            )
        with gr.Column(scale=2):
            model_dropdown = gr.Dropdown(
                choices=[""] + openai_models,
                label="Select OpenAI Model for generation (optional)",
            )

    with gr.Row():
        with gr.Column(scale=2):
            posts_output = gr.HTML(elem_id="posts-container")

    with gr.Row():
        with gr.Column(scale=1):
            post_user_input = gr.Textbox(label="Post anything yourself")
            post_user_dropdown = gr.Dropdown(
                choices=[""] + list(users.keys()),
                label="Select User for Post",
            )
            post_button = gr.Button("Create Post")

        with gr.Column(scale=1):
            reply_post_id = gr.Textbox(
                label="Post ID to Reply To", placeholder="Enter Post ID"
            )
            reply_user_input = gr.Textbox(label="Reply to the post yourself")
            reply_user_dropdown = gr.Dropdown(
                choices=[""] + list(users.keys()) + ["All Users"],
                label="Select User for Reply",
            )
            reply_button = gr.Button("Create Reply")

    post_button.click(
        create_post,
        inputs=[post_user_dropdown, post_user_input, model_dropdown],
        outputs=posts_output,
    ).then(lambda: (None, None), outputs=[post_user_input, post_user_dropdown])
    reply_button.click(
        create_reply,
        inputs=[reply_post_id, reply_user_dropdown, reply_user_input, model_dropdown],
        outputs=posts_output,
    ).then(
        lambda: (None, None, None),
        outputs=[reply_post_id, reply_user_input, reply_user_dropdown],
    )

    app.queue()

if __name__ == "__main__":
    app.launch()
