all:
	python webpage/deploy.py

test:
	pytest

pylint:
	pylint webpage

pyflakes:
	pyflakes webpage

mypy:
	mypy webpage

doc:
	cd docs; make html; cd -

cleandoc:
	rm -rf docs/_build

clean:
	rm -rf html tests/*~ webpage/*~
