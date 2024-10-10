def printpost(user, post):
    print(
        f"{colors['CYELLOWBG']} User {user.username} {colors['CEND']} posted: "
        f"{colors['CYELLOW']}{post.content}{colors['CEND']}"
    )


def printreply(user, post, reply):
    print(
        f"{colors['CBLUEBG']}User {user.username}{colors['CEND']} replied to "
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
