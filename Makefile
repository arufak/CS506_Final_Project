install:
	python3 -m venv venv
ifeq ($(OS),Windows_NT)
	venv\Scripts\activate && pip install -r requirements.txt
else
	. venv/bin/activate && pip install -r requirements.txt
endif

run:
ifeq ($(OS),Windows_NT)
	venv\Scripts\activate && set FLASK_APP=app.py && flask run --host=0.0.0.0 --port=3000
else
	. venv/bin/activate && FLASK_APP=app.py flask run --host=0.0.0.0 --port=3000
endif

clean:
ifeq ($(OS),Windows_NT)
	rmdir /S /Q venv
else
	rm -rf venv
endif
