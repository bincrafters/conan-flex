#!/usr/bin/env bash

set -ex

pip install --upgrade pip
python --version
pip --version

if [[ "$(uname -s)" == 'Darwin' ]]; then
    rm -rf /usr/local/opt/pyenv;
    rm /usr/local/bin/pyenv;
    rm /usr/local/bin/pyenv-install;
    rm /usr/local/bin/pyenv-uninstall;
    ln -s /usr/local/opt/pyenv/libexec/pyenv /usr/local/bin/pyenv;
    unset PYENV_ROOT;
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash;
    export PATH="$HOME/.pyenv/bin:$PATH";
    eval "$(pyenv init -)";
    eval "$(pyenv virtualenv-init -)";
    pyenv --version;
    pyenv install 3.7.5;
    pyenv virtualenv 3.7.5 conan;
    pyenv rehash;
    pyenv activate conan;
    pip install cmake --upgrade;
fi

pip install bincrafters_package_tools

conan user
