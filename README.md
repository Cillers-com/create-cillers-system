# Cillers Create System

## Instructions

### Prerequisites
Make sure you have [Docker](https://www.docker.com/) and the latest version of [Polytope](https://polytope.com) installed on your system. 

[Install Docker](https://docs.docker.com/engine/install/)

Install Polytope:
```
brew tap polytopelabs/tap
brew install polytope-cli
```

### Create your Cillers system
```
pt run "cillers/create-system{name: my_system}"
```
Stop Polytope with `ctrl-c`

### Run the stack
```
cd my_system
pt run stack
```
This will take a little while the first time (depending on your network speed) as all the components of the stack are downloaded.

### Open the web UIs
Web frontend: http://localhost/ (Create new account)  
GraphQL: http://localhost:4000/api ({ "Authorization": "Bearer xxx" })  
Curity: https://localhost:6749/admin (username: admin, password: password)  
Mailpit: http://localhost:8025/   
Couchbase: http://localhost:8091/ (username: admin, password: password)  

You will of course want to change the above passwords. 

### Troubleshooting
You may have to reinstall Polytope
```
brew uninstall polytope-cli
brew untap polytopelabs/tap
brew tap polytopelabs/tap
brew install polytope-cli
```

On OSX and Windows, you need to make sure that the Docker VM has enough memory to run the full stack. See [here](https://docs.docker.com/desktop/settings/mac/#resources) for instructions on how to allocate more memory.
