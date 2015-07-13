from snake import *
import string
import re


COLOR_PREFIX = "cuttlefish"

COLORS = ["ctermfg=1", "ctermfg=2",
          "ctermfg=3", "ctermfg=4",
          "ctermfg=5", "ctermfg=6",
          "ctermfg=7",
          "ctermfg=1 cterm=underline", "ctermfg=2 cterm=underline",
          "ctermfg=3 cterm=underline", "ctermfg=4 cterm=underline",
          "ctermfg=5 cterm=underline", "ctermfg=6 cterm=underline",
          "ctermfg=7 cterm=underline"]


def toggle_semantic_highlight(**kwargs):
    try:
        raw_output = command("silent hi %s_0" % COLOR_PREFIX, capture=True)
        active = "cleared" not in raw_output
    except:
        active = False
    if active:
        deactivate_semantic_highlight()
    else:
        activate_semantic_highlight(**kwargs)


def define_colors():
    for nr, color in enumerate(COLORS):
        command("hi! def %s_%s %s ctermbg=0" % (COLOR_PREFIX, nr, color))


def clear_colors():
    for nr, color in enumerate(COLORS):
        command("hi! clear %s_%s" % (COLOR_PREFIX, nr))


def deactivate_semantic_highlight():
    clear_colors()
    command("syn on")


def activate_semantic_highlight(clear_keyword_defs=True):
    command(":py from snake.plugins import vim_cuttlefish")
    command(":autocmd InsertLeave,InsertEnter,BufWritePost * :py vim_cuttlefish.activate_semantic_highlight()")
    define_colors()
    last_color = len(COLORS)

    blacklists = {
        "python": ["True", "False", "def", "import", "try", "except", "if", "else", "from", "class", "return", "not", "in", "for", "pass", "continue", "break", "while", "with", "as"]
    }

    try:
        filetype = get_filetype()
    except Exception as e:
        command("print AAARRRGGGHHH")
        filetype = "python"
    blacklist = blacklists.get(filetype, set())

    buffer = get_current_buffer()

    if blacklist and clear_keyword_defs:
        command("syn keyword _ %s" % " ".join(blacklist))

    tokencount = {}
    for line in get_buffer_lines(buffer):
        line = line.strip()
        if line.startswith("#"):
            continue
        line = re.sub("[a-zA-Z0-9]+\(", "", line)
        line = re.sub("[ \.\t,;()\[\]{}=\|\"\']+", " ", line)
        for token in line.split():
            token = token.strip()
            if not token:
                continue
            blacklisted = False
            for blacklist_item in blacklist:
                if re.match(blacklist_item, token):
                    blacklisted = True
                    break
            if blacklisted:
                continue
            # if token in blacklist:
                # continue
            if token[0] in ["\"", "%", "@", "\\", "\'", "&"]:
                continue
            letter_found = False
            for c in token:
                if c in string.letters:
                    letter_found = True
                    break
            if not letter_found:
                continue
            # if token.isdigit():
                # continue
            tokencount[token] = tokencount.get(token, 0) + 1

    token2color = {}
    current = 0
    for token, count in tokencount.items():
        if count <= 0:
            continue
        token2color[token] = "%s_%s" % (COLOR_PREFIX, current)
        current = (current + 1) % last_color

    for token, color in token2color.items():
        command("syn keyword %s %s" % (color, token))

    with open("vimrcpy.log", "w") as logfile:
        logfile.write("filetype: '%s'\n" % filetype)
        color2tokens = {}
        for token, color in token2color.items():
            if not color in color2tokens:
                color2tokens[color] = []
            color2tokens[color].append(token)
        for color in sorted(color2tokens):
            tokens = color2tokens[color]
            logfile.write("color %s: %s\n" % (color, ", ".join(tokens)))


def get_filetype():
    with preserve_registers("a"):
        vim.command("redir @a")
        vim.command("silent echo &filetype")
        vim.command("redir END")
        return get_register("a").strip()
    # return command("echo &filetype", capture=True)   # does not work *strange*


def list_all_colors():
    lines =  []
    for i in range(255):
        lines.append("color%s" % i)
        command("hi! def listcolors%s ctermfg=%s" % (i, i))
        command("syn keyword listcolors%s color%s" % (i, i))
    set_buffer_lines(buffer, lines)
