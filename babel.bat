#pybabel init -i lang/messages.pot -d lang/translations -l ja

pybabel extract -F babel.cfg -k lazy_gettext -o lang/messages.pot --ignore-dirs="env .env venv genv" .
pybabel update -i lang/messages.pot -d lang/translations
pybabel compile -d lang/translations