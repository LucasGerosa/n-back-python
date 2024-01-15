function check_python {
	python_name=$(which python)
	if [ "$python_name" = "" ]; then
		python_name=$(which python3)
		if [ "$python_name" = "" ]; then
			python_name=$(which py)
			if [ "$python_name" = "" ]; then
				sudo apt install python3
				return check_python
			fi		
		fi
	fi
}
check_python

venv_name="venv"
PROJECT_DIR=$(dirname -- "$0")
if [ "$VIRTUAL_ENV" = "" ]
then
	if [ -d "$PROJECT_DIR/venv" ]; then
		echo "venv path exists"
	else
		echo "venv doesn't exist. Creating it now."
		$python_name -m venv $venv_name
	fi
else
echo "in venv"
fi