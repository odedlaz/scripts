#!/bin/bash
USER=odedlaz

function update_neovim {
   export WORKON_HOME="$HOME/.virtualenvs"
   export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
   source /usr/local/bin/virtualenvwrapper.sh
   source "$HOME/.funcrc"

   update_python_packages "neovim2"
   update_python_packages "neovim3"
}

if apt list --upgradable 2>/dev/null | grep "[n]eovim" &>/dev/null; then
   echo "Updating neovim python libraries..."
   export -f update_neovim
   su $USER -c "bash -c update_neovim"
fi
