deploy:
	caprover deploy --caproverName rossini --caproverApp roadmap --branch main

run:
	python3 -m better_roadmap

docker-build:
	docker build . -t rodelrod/better-roadmap:0.1

docker-run:
	docker run -d -p 5000:5000 rodelrod/better-roadmap:0.1

docker-inspect:
	docker run -it rodelrod/better-roadmap:0.1 bash
