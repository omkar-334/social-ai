def post_prompt(user, words):
    user_prompt = f"""
    You need to create a new post. 
    Your previous posts were:\n{user.construct_post_history()}

    Your new post should be relevant to your interests: {", ".join(user.interests)}.
    Ensure the content is unique and does not repeat the topics or style of your previous posts.
    Be creative, and vary the content to explore different aspects of your interests. 
    Feel free to express a new angle or a fresh opinion on something you haven't discussed yet.
    Do not include hashtags, @ , mentions, markdown formatting, bold, italic, etc. Answer in plaintext.
    Make sure your post is under {words} words.

    """

    return user_prompt


def reply_prompt(user, post, words):
    #  The post's previous replies are:\n{post.construct_reply_history()}
    user_prompt = f"""
    You need to directly reply to a post.
    The post's content is - "{post.content}".

    Create a unique response directly related to the post's content, contributing something new to the conversation.

    Ensure that your decision, reply (if you choose to reply) fits your communication style ({user.communication_style}). Be creative, and avoid repeating ideas that have already been discussed.
    Do not add "Re", the post's title, quotes or anything indicating to refer to the post. 
    Make sure your reply is under {words} words.
    """
    return user_prompt


def system_prompt(user):
    interest_prompt = (
        f"You are interested in: {', '.join(user.interests)}. "
        if user.interests
        else "You haven't listed any specific interests. "
    )

    style_prompt = (
        "You are proactive on social media. You initiate posts and conversations. "
        if user.engagement_style == "proactive"
        else "You are reactive on social media. You prefer responding to other posts rather than starting your own"
    )

    prompt = f"""
    You are {user.username}.
    You are described as: {user.bio}.
    {interest_prompt}
    Your communication style is {user.communication_style}.
    You are {user.engagement_level} on social media.
    {style_prompt}
    Your response speed is generally {user.response_speed} ."""

    return prompt
