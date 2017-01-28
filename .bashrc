# Load up standard site-wide settings.
source /etc/bashrc

#remove duplicate entries from history
export HISTCONTROL=ignoreboth

# Show current git branch in prompt.
function parse_git_branch {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
RED="\[\033[0;31m\]"
YELLOW="\[\033[0;33m\]"
GREEN="\[\033[0;32m\]"
LIGHT_GREEN="\[\033[1;32m\]"
LIGHT_GRAY="\[\033[0;37m\]"

PS1="$LIGHT_GRAY\$(date +%H:%M) \w$YELLOW \$(parse_git_branch)$LIGHT_GREEN\$ $LIGHT_GRAY"

# Load virtualenvwrapper
source virtualenvwrapper.sh &> /dev/null

export
DJANGO_SITE=$HOME/mysite
EMU_SITE=$HOME/Emu86

export
PYTHONPATH=$PYTHONPATH:$HOME/Indra:$DJANGO_SITE:$DJANGO_SITE/berkeley:

export DJANGO_SETTINGS_MODULE=mysite.settings

alias gpull="git pull origin master"
alias gpush="git push origin master"

alias alg="cd $HOME/algorithms"

alias doc="cd $HOME/Indra/docs"
alias ind="cd $HOME/Indra/indra"
alias sch="cd $HOME/Indra/schelling"

alias sta="cd $HOME/statistics"

alias emu="cd $EMU_SITE/Emu86"
alias etem="cd $EMU_SITE/Emu86/templates"
alias ecss="cd $EMU_SITE/mysite/static/Emu86"

alias css="cd $DJANGO_SITE/mysite/static/berkeley"
alias ber="cd $DJANGO_SITE/berkeley"
alias mig="cd $DJANGO_SITE/berkeley/migrations"
alias sit="cd $DJANGO_SITE/mysite"
alias tem="cd $DJANGO_SITE/berkeley/templates"
alias top="cd $DJANGO_SITE"

workon django19
