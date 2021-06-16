# kong_min

in order to create service:
    POST call to http://localhost:8001/services/
    with body {
        "name": "api",
        "host":"kong_min_api_1",
        "port": 5000
    } 


in order to create route (needs a service):
    POST to http://localhost:8001/services/api/routes
    with body {
        "name":"first",
        "paths":["/route-two"]
        #"methods": ["POST"],
        #"strip_path": false #by default to true (removes /route-two from url)
    }


and then a call to 0.0.0.0:8000/my-route/route-one will be redirected to 0.0.0.0:5000/route-one