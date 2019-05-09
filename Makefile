test:
	pytest

doc:
	cd docs; make html; cd -

cleandoc:
	rm -rf docs/_build

clean:
	rm -rf html tests/*~ webpage/*~
