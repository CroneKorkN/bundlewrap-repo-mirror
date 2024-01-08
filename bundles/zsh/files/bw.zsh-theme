function zsh_spwd {
  paths=(${(s:/:)PWD})

  cur_path='/'
  cur_short_path='/'
  for directory in ${paths[@]}
  do
    cur_dir=''
    for (( i=0; i<${#directory}; i++ )); do
      cur_dir+="${directory:$i:1}"
      matching=("$cur_path"/"$cur_dir"*/)
      if [[ ${#matching[@]} -eq 1 ]]; then
        break
      fi
    done
    cur_short_path+="$cur_dir/"
    cur_path+="$directory/"
  done

  printf %q "${cur_short_path: : -1}"
  echo
}

function zsh_root_color {
  if test "$EUID" -eq 0
  then
    echo "%{$fg_bold[green]%}"
  else
    echo "%{$fg_bold[yellow]%}"
  fi
}

function zsh_exitcode_color {
  echo "%(?:%{$fg_bold[green]%}:%{$fg_bold[red]%})"
}

function zsh_hostname {
  if [ -z "$ZSH_HOSTNAME" ]
  then
    hostname -s
  else
    echo "$ZSH_HOSTNAME"
  fi
}

PROMPT='$(zsh_root_color)$(whoami)%{$reset_color%}@$(zsh_exitcode_color)$(zsh_hostname) %{$fg[cyan]%}$(zsh_spwd)%{$reset_color%} $(git_prompt_info)'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
