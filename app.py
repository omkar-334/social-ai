import gradio as gr

import main
from network import AppNetwork
from post import Post

simulation = AppNetwork(main.users)


def format_message(username, content, icon_url="icon.png"):
    return f"""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <img src="{icon_url}" style="width: 32px; height: 32px; border-radius: 50%; margin-right: 10px;">
        <div style="display: flex; flex-direction: column;">
            <p style="color: yellow; font-size: 16px; margin: 0; font-weight: bold; line-height: 1;">{username}</p>
            <p style="margin: 4px 0 0 0; font-size: 14px; line-height: 1.3;">{content}</p>
        </div>
    </div>
    """


async def update_interface(posts_display):
    post_ids = []
    async for item in simulation.start():
        if isinstance(item, Post):
            posts_display.append((format_message(item.author, item.content), None))
            post_ids.append(item.id)
        yield posts_display, gr.update(choices=post_ids)


def get_post_replies(post_id):
    if post_id:
        post = simulation.posts_dict[post_id]
        return [
            (format_message(reply.author, reply.content), None)
            for reply in post.replies
        ]
    return []


async def stop_simulation():
    await simulation.stop()
    return gr.update(interactive=True), gr.update(interactive=False)


with gr.Blocks() as app:
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            posts_display = gr.Chatbot(label="Posts", height=600)
        with gr.Column(scale=1):
            posts_dropdown = gr.Dropdown(
                label="Select Post", choices=[], interactive=True
            )
            replies_display = gr.Chatbot(label="Replies", height=520)

    with gr.Row():
        start_button = gr.Button("Start Simulation")
        stop_button = gr.Button("Stop Simulation", interactive=False)

    start_button.click(
        update_interface,
        inputs=[posts_display],
        outputs=[posts_display, posts_dropdown],
    ).then(
        lambda: (gr.update(interactive=False), gr.update(interactive=True)),
        outputs=[start_button, stop_button],
    )

    stop_button.click(stop_simulation, outputs=[start_button, stop_button])

    posts_dropdown.change(
        get_post_replies, inputs=[posts_dropdown], outputs=[replies_display]
    )

if __name__ == "__main__":
    app.queue().launch(height=750)
