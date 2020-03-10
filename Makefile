deploy:
	git pull
	docker-compose down
	docker-compose pull web
	docker-compose up -d

translate:
	pybabel extract -F blog/babel.cfg -k lazy_gettext -o messages.pot blog/
	pybabel update -i messages.pot -d blog/translations
	rm messages.pot

compile:
	pybabel compile -d blog/translations

.PHONY: deploy translate compile
