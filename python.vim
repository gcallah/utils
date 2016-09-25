" mappings for python editing

let python_highlight_all=1

noremap R :w<ENTER>:!python %
map # o"""<CR>    Args:<CR><CR><Esc>i        Returns:<CR><CR><Esc>i    """<Esc>
map  idef ():ki
map  oimport
map  oprint("")hi
map <F1> oif :i
map <F2> oelif :i
map <F3> oelse:


