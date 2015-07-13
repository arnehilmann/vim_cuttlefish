![a cute cuttlefish](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Cuttlefish_%40_Ocean%C3%A1rio_de_Lisboa.jpg/255px-Cuttlefish_%40_Ocean%C3%A1rio_de_Lisboa.jpg)

# vim_cuttlefish

aka generic-semantic-highlighting.vim, but thats not a good python package name, so cuttlefish it is
https://en.wikipedia.org/wiki/Cuttlefish#Colouration


## tl;dr

- install the [snake plugin for vim](https://github.com/amoffat/snake)

- install this plugin

  - using [vundle](https://github.com/VundleVim/Vundle.vim):
     add ```"Plugin 'arnehilmann/vim_cuttlefish'"``` to your vundle plugin definition

- in your $HOME/.vimrc.py, import this plugin and map a key
```bash
from snake import *
from snake.plugins import vim_cuttlefish as cuttlefish

# here: map <leader>-S to the semantic highlighting function
@key_map("<leader>S")
def toggle_gensemhl():
    cuttlefish.toggle_semantic_highlight()
```
