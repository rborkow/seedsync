all:
ifdef VIRTUAL_ENV
	@echo "No setup required."
	@exit
else
	@virtualenv venv
endif

pip:
	@pip install --upgrade pip
	@pip install -r requirements.txt
	
clean:
	@virtualenv --clear venv
