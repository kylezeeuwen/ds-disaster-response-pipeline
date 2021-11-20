#!/bin/sh

virtualenv=${1:-dsstackoverflow}
pyenv init -
pyenv virtualenv-init -

if type pyenv
then
	if pyenv virtualenvs
	then
		python_version=3.9.5
		venv_name=$python_version/envs/$virtualenv
		pyenv install $python_version --skip-existing
		pyenv virtualenv --force $python_version $virtualenv && \
			pyenv activate $venv_name && \
			pip3 install -r requirements.txt && \
			pyenv deactivate $venv_name && \
			echo $venv_name > .python-version
	else
		echo "Pyenv requires pyenv-virtualenv to set up virtualenvs. Exiting..."
		exit 1
	fi
else
	echo "WARNING: a virtual environment created by pyenv is recommended for running this script"
fi

pip3 install -r requirements.txt
