# Polytope-Apollo-Couchbase-Curity

## Instructions
Make sure you have [Docker](https://docs.docker.com/engine/install/) installed on your system.

Install the Polytope CLI:
```
brew tap mjosefs/polytope
brew install polytope-cli
```

Run the stack:
```
pt run --local dev
```
This will take a little while the first time (depending on your network speed) as all the components of the stack are downloaded.

### Notes
- On OSX/Windows, the Docker VM might not have enough memory to run the full stack. See [here](https://docs.docker.com/desktop/settings/mac/#resources) for instructions on how to allocate more memory.
