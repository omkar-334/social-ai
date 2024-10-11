def printpost(post):
    print(
        f"{colors['CYELLOWBG']} User {post.author.name} {colors['CEND']} posted: "
        f"{colors['CYELLOW']}{post.content}{colors['CEND']}"
    )


def printreply(post, reply):
    print(
        f"{colors['CBLUEBG']}User {post.author.name}{colors['CEND']} replied to "
        f"{colors['CYELLOWBG']}{post.author}'s{colors['CEND']} post: "
        f"{colors['CBLUE']}{reply.content}{colors['CEND']}"
    )


colors = dict(
    CEND="\33[0m",
    CBOLD="\33[1m",
    CITALIC="\33[3m",
    CURL="\33[4m",
    CBLINK="\33[5m",
    CBLINK2="\33[6m",
    CSELECTED="\33[7m",
    CBLACK="\33[30m",
    CRED="\33[31m",
    CGREEN="\33[32m",
    CYELLOW="\33[33m",
    CBLUE="\33[34m",
    CVIOLET="\33[35m",
    CBEIGE="\33[36m",
    CWHITE="\33[37m",
    CBLACKBG="\33[40m",
    CREDBG="\33[41m",
    CGREENBG="\33[42m",
    CYELLOWBG="\33[43m",
    CBLUEBG="\33[44m",
    CVIOLETBG="\33[45m",
    CBEIGEBG="\33[46m",
    CWHITEBG="\33[47m",
)

user_colors = [
    "#FF4136",  # Bright Red
    "#FF851B",  # Bright Orange
    "#FFDC00",  # Bright Yellow
    "#2ECC40",  # Lime Green
    "#00FF7F",  # Spring Green
    "#39CCCC",  # Teal
    "#7FDBFF",  # Sky Blue
    "#0074D9",  # Bright Blue
    "#B10DC9",  # Purple
    "#F012BE",  # Fuchsia
    "#FF69B4",  # Hot Pink
    "#FF85FF",  # Light Pink
    "#FF4500",  # Orange Red
    "#00FF00",  # Lime
    "#FFD700",  # Gold
    "#00FFFF",  # Cyan
    "#1E90FF",  # Dodger Blue
    "#FF1493",  # Deep Pink
    "#ADFF2F",  # Green Yellow
    "#FFA500",  # Orange
    "#FF00FF",  # Magenta
    "#00CED1",  # Dark Turquoise
    "#FF6347",  # Tomato
    "#40E0D0",  # Turquoise
    "#7FFF00",  # Chartreuse
    "#FF8C00",  # Dark Orange
    "#BA55D3",  # Medium Orchid
    "#32CD32",  # Lime Green
    "#FFB6C1",  # Light Pink
    "#87CEFA",  # Light Sky Blue
]
