all:
ifdef VIRTUAL_ENV
	@echo "No setup required."
	@exit
else
	@virtualenv venv
	@pip install --upgrade pip
	@pip install -r requirements.txt
endif

clean:
	@virtualenv --clear venv
