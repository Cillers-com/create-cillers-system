# Cillers Create System

## Instructions

### Prerequisites
Make sure you have Docker and the latest version of Polytope installed on your system. 

[Docker](https://docs.docker.com/engine/install/)

Polytope
```
brew tap mjosefs/polytope
brew install polytope-cli
```

### Create a Cillers system
```
pt run "cillers/create-system{name: my_system}
```
Stop Polytope with ctrl-c

### Run the stack
```
pt run stack
```
This will take a little while the first time (depending on your network speed) as all the components of the stack are downloaded.

### Open the web UIs
Web frontend: http://localhost/ (Create new account)
GraphQL: http://localhost:4000/api ({ "Authorization": "Bearer xxx" })
Curity: https://localhost:6749/admin (username: admin, password: password)
Mailpit: http://localhost:8025/ 
Couchbase: http://localhost:8091/

### Notes
- On OSX/Windows, the Docker VM might not have enough memory to run the full stack. See [here](https://docs.docker.com/desktop/settings/mac/#resources) for instructions on how to allocate more memory.

### Troubleshooting
You may have to reinstall Polytope
```
brew uninstall polytope-cli
brew untap mjosefs/polytope
brew tap mjosefs/polytope
brew install polytope-cli
```