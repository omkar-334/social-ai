import gradio as gr

from network import AppNetwork
from post import Post, Reply
from users import users

simulation = AppNetwork(users)


def format_message(username, content, is_reply=False, icon_url="icon.png"):
    # Adjust CSS for replies (indentation, smaller font size)
    margin_left = "30px" if is_reply else "0"
    font_size = "14px" if is_reply else "16px"
    username_color = "#aaa" if is_reply else "yellow"  # Different color for replies
    return f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 10px; margin-left: {margin_left};">
        <img src="{icon_url}" style="width: 28px; height: 28px; border-radius: 50%; margin-right: 10px;">
        <div style="display: flex; flex-direction: column; flex-grow: 1;">
            <p style="color: {username_color}; font-size: {font_size}; margin: 0; font-weight: bold; line-height: 1;">{username}</p>
            <p style="margin: 4px 0 0 0; font-size: 13px; line-height: 1.3;">{content}</p>
        </div>
    </div>
    """


async def update_interface():
    posts_content = ""
    posts_dict = {}

    async for item in simulation.start():
        if isinstance(item, Post):
            posts_dict[item.id] = format_message(item.author, item.content)

        if isinstance(item, Reply):
            if item.postid in posts_dict:
                posts_dict[item.postid] += format_message(
                    item.author, item.content, is_reply=True
                )

        # Combine all posts and their replies
        posts_content = "".join(posts_dict.values())

        # Update the posts container with all posts and replies
        posts_html = f"""
        <div style="height: 600px; overflow-y: auto; padding: 10px; background-color: #1a1a1a; border-radius: 10px;">
            {posts_content}
        </div>
        """
        yield posts_html


async def stop_simulation():
    await simulation.stop()
    return gr.update(interactive=True), gr.update(interactive=False)


with gr.Blocks(css="#posts-container {height: 600px; overflow-y: auto;}") as app:
    with gr.Row():
        with gr.Column(scale=2):
            posts_html = gr.HTML(elem_id="posts-container")

    start_button = gr.Button("Start Simulation")
    stop_button = gr.Button("Stop Simulation", interactive=False)

    start_button.click(
        update_interface,
        outputs=[posts_html],
    ).then(
        lambda: (gr.update(interactive=False), gr.update(interactive=True)),
        outputs=[start_button, stop_button],
    )

    stop_button.click(stop_simulation, outputs=[start_button, stop_button])

app.queue()

if __name__ == "__main__":
    app.launch(height=750)
