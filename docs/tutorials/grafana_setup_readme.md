## FastAPI, Prometheus, Grafana with docker-compose


#### What is this?

An example of how to run FastAPI, Prometheus and Grafana with docker-compose.


#### Prerequisites
* Install docker: https://docs.docker.com/engine/install/


#### How to run it

```bash
# clone repo and launch containers:

$ git clone https://github.com/L00188483/grafana_test.git
$ cd grafana_test/

docker compose up

```


### Testing that it works

###### Checking containers
```bash
# verify 3 containers are running:

$ docker ps

CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS                                         NAMES
af69a7926293   grafana/grafana-enterprise   "/run.sh"                20 seconds ago   Up 20 seconds   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   grafana
e17684a91cd1   prom/prometheus              "/bin/prometheus --c…"   20 seconds ago   Up 20 seconds   0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp   prometheus
6b7fe0831a88   grafana_test-webapp          "uvicorn app.main:f_…"   20 seconds ago   Up 20 seconds   0.0.0.0:80->80/tcp, [::]:80->80/tcp           webapp
```

###### Do some health checks
```bash
# check webapp is running 
$ curl  http://localhost:80/hello/anna
{"hello":"anna"}

# check metrics are available at /metrics
$ curl  http://localhost:80/metrics

# check health of Promethues
$ curl http://localhost:9090/-/healthy
Prometheus Server is Healthy.

# check health of Grafana
$ curl http://localhost:3000/api/health
{
  "database": "ok",
  "version": "11.5.1",
  "commit": "c6c701cf5be984b088b9d51690b474ab63ca86ff",
  "enterpriseCommit": "f8db9a5ff8fd548b469344667730a52dc2f1c85b"
}
```

###### Inspect the dashboards in the browser

###### Prometheus
* Go to: http://localhost:9090/
* Click the 3 dots next to the blue "Execute" button on the right
* Click "Explore metrics"
* Copy/paste "http_request_duration_seconds_bucket" in the query box and click "Execute"

###### Grafana
* Go to: http:localhost:3000/
* login with "admin" and "admin_pass"
* Click "Add your first data source" on the right
* Choose "Prometheus"
* Enter the "Prometheus server URL" as: "http://prometheus:9090" (this is its docker hostname)
* Scroll to the bottom and click "Save & test"
* Click the link to the "Explore view"
* Select the "Metrics Browser"
* Click "http_request_duration_seconds_bucket"
* Click "Use query"
* You should now see a data graph


#### Cleaning up: how to remove all containers and volumes

```bash

$ chmod +x docker_remove_all.sh
$ ./docker_remove_all.sh
```
