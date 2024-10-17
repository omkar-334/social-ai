import asyncio

import gradio as gr

from network import AppNetwork
from profiles import users

simulation = AppNetwork(users)


def format_message(item, is_reply=False):
    margin_left = "30px" if is_reply else "0"
    font_size = "14px" if is_reply else "16px"

    icon_html = f'<img src="{item.author.icon_url}" style="width: 28px; height: 28px; border-radius: 50%; margin-right: 10px;">' if item.author.icon_url else ""

    message_html = f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 10px; margin-left: {margin_left};">
        {icon_html}
        <div style="display: flex; flex-direction: column; flex-grow: 1;">
            <p style="color: {item.author.color}; font-size: {font_size}; margin: 0; font-weight: bold; line-height: 1;">{item.author.name}</p>
            <p style="margin: 4px 0 0 0; font-size: 13px; line-height: 1.3;">{item.content}</p>
    """

    if not is_reply:
        message_html += f"""
            <p style="font-size: 10px; color: gray;">Post ID: <span style="text-transform: lowercase;">{item.id}</span>
            <button onclick="navigator.clipboard.writeText('{item.id}')" style="margin-left: 5px; font-size: 10px;">Copy</button></p>
        """

    message_html += "</div></div>"
    return message_html


async def create_post(selected_user):
    if selected_user == "Select User":
        selected_user = None
    await simulation.create_post(selected_user)
    return update_interface()


async def create_reply(post_id, selected_user):
    if selected_user == "All Users":
        tasks = [simulation.create_reply(post_id, user_name) for user_name in users.keys()]
        await asyncio.gather(*tasks)
    else:
        if selected_user == "Select User":
            selected_user = None
        await simulation.create_reply(post_id, selected_user)
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


with gr.Blocks(css="#posts-container {height: 400px; overflow-y: auto;}") as app:
    gr.Markdown("## Social Network Simulation\n\nDon't select a user if you want a random user.")
    with gr.Row():
        with gr.Column(scale=2):
            posts_output = gr.HTML(elem_id="posts-container")

    with gr.Row():
        with gr.Column(scale=1):
            post_user_dropdown = gr.Dropdown(choices=["Select User"] + list(users.keys()), label="Select User for Post")
            post_button = gr.Button("Create Post")

        with gr.Column(scale=1):
            reply_post_id = gr.Textbox(label="Post ID to Reply To", placeholder="Enter Post ID")
            reply_user_dropdown = gr.Dropdown(choices=["Select User"] + list(users.keys()) + ["All Users"], label="Select User for Reply")
            reply_button = gr.Button("Create Reply")

    post_button.click(create_post, inputs=post_user_dropdown, outputs=posts_output)
    reply_button.click(create_reply, inputs=[reply_post_id, reply_user_dropdown], outputs=posts_output)

    app.queue()

if __name__ == "__main__":
    app.launch(height=600)
