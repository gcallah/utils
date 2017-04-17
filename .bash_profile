
# Setting PATH for Python 3.4
# The orginal version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.4/bin:${PATH}"
export PATH

export GDIR="$HOME/GitProjects"

set editing-mode vi

alias pro=". ~/.bash_profile"

alias agl="cd $GDIR/AgileCourseware"
alias alg="cd $GDIR/algorithms"
alias ass="cd $GDIR/Emu86/assembler"
alias book="cd $GDIR/BookReviews"
alias box="cd $GDIR/indra/bigbox"
alias emu="cd $GDIR/Emu86"
alias doc="cd $GDIR/indra/docs"
alias four="cd $GDIR/FourCritics"
alias ftp="cd ~/.vim/after/ftplugin/"
alias gca="cd $GDIR/gcallah.github.io"
alias gen="cd $GDIR/GenericProgramming/generic"
alias his="cd $GDIR/history_of_science"
alias hsc="cd $GDIR/HotScheme"
alias ind="cd $GDIR/indra"
alias indl="cd $GDIR/indra/indra"
alias kic="cd $GDIR/KickingTheStone"
alias mat="cd $GDIR/matplotlib/doc/users"
alias mdl="cd $GDIR/indra/models"
alias mes="cd $GDIR/mesa/examples"
alias os="cd $GDIR/OperatingSystems"
alias rat="cd $GDIR/Rationalism"
alias sch="cd $GDIR/indra/schelling"
alias sta="cd $GDIR/statistics"
alias utl="cd $GDIR/utils"
alias xv6="cd $GDIR/xv6-public"

alias ga="git add"
alias gc="git commit"
alias gco="git checkout"
alias gpushm="git push origin master"
alias gpullm="git pull origin master"
alias gpushd="git push origin dev"
alias gpulld="git pull origin dev"
alias gs="git status"

# added by Anaconda3 2.1.0 installer
export PATH="/Users/gcallah/anaconda/bin:$PATH"

export PYTHONPATH="$GDIR/indra:$GDIR/mesa:$PYTHONPATH"

export PATH="/Users/gcallah/gcc-cross/toolchain/bin":"$PATH"

export PATH="/Users/gcallah/GitProjects/utils":"$PATH"

# Tidy for Mac OS X by balthisar.com is adding the new path for Tidy.
export PATH=/usr/local/bin:$PATH

