test:
	@pre-commit run --all-files

install:
	@pip3 install -r requirements.txt

run:
	@python3 -m skynoid

update:
	@git pull
	@pip3 install -U -r requirements.txt
