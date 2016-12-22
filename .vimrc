set nocompatible
set noerrorbells visualbell t_vb=
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
" Plugin 'Lokaltog/vim-easymotion'
" Plugin 'tpope/vim-fugitive.git'
" Plugin 'scrooloose/nerdtree'
" Plugin 'scrooloose/syntastic'
" Plugin 'nvie/vim-flake8'
Plugin 'tpope/vim-surround.git'
Plugin 'tpope/vim-repeat.git'
Plugin 'vim-scripts/indentpython.vim'
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'
call vundle#end()            " required
filetype plugin indent on    " required

filetype plugin on

set number
set history=50
set shiftwidth=4
set tabstop=4
set softtabstop=4
set textwidth=79
set expandtab
set autoindent
set fileformat=unix
set showcmd
set backup
set noshowmatch
" set incsearch
set hlsearch
set scrolloff=8
set pastetoggle=<f5>
set encoding=utf-8

syntax on

if has('gui_running')
    set background=dark
    colorscheme solarized
else
    colorscheme zenburn
endif

" noremap R :w<ENTER>:!python %

filetype plugin indent on
let loaded_matchparen = 1
noremap #5 :!./%

function! ToggleSyntax()
    if exists("g:syntax_on")
        syntax off
    else
        syntax enable
    endif
endfunction

nmap <silent>  ;s  :call ToggleSyntax()<CR>
