" mappings for python editing

let python_highlight_all=1

noremap R :w<ENTER>:!python %

" grep
map g :!grep 

map # o"""<CR>    Args:<CR><CR><Esc>i        Returns:<CR><CR><Esc>i    """<Esc>
map  idef ():ki
map  oimport
" insert an empty line
map  o
map  oprint("")hi
map <F1> oif :hi
map <F2> oelif :hi
map <F3> oelse:
map <F4> ofor i in range(0, n):
map <F5> def __init__(self, ):2hi


