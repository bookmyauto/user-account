default:
	python3 main.py

docker-push:
	cat keyfile.json | docker login -u _json_key --password-stdin https://asia.gcr.io
	docker build -t user-account .
	docker tag user-account asia.gcr.io/bookmyauto-test/user-account:$(TAG)
	docker push asia.gcr.io/bookmyauto-test/user-account:$(TAG)
