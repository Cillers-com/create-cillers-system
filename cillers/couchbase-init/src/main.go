package main

import (
    "fmt"
    "os"
    "strings"

    "couchbase-init/lib/controllers"
)

type Config struct {
    username   string
    password   string
    host       string
    tls        bool
    bucketName string
    cType      string
}

func getEnvVar(name string) (string, error) {
    value := os.Getenv(name)
    if value == "" {
        return "", fmt.Errorf("environment variable '%s' is not set", name)
    }
    return value, nil
}

func loadConfig() (Config, error) {
    username, err := getEnvVar("COUCHBASE_USERNAME")
    if err != nil {
        return Config{}, err
    }
    
    password, err := getEnvVar("COUCHBASE_PASSWORD")
    if err != nil {
        return Config{}, err
    }
    
    host, err := getEnvVar("COUCHBASE_HOST")
    if err != nil {
        return Config{}, err
    }
    
    tlsStr, err := getEnvVar("COUCHBASE_TLS")
    if err != nil {
        return Config{}, err
    }
    
    bucketName, err := getEnvVar("COUCHBASE_MAIN_BUCKET_NAME")
    if err != nil {
        return Config{}, err
    }
    
    cType, err := getEnvVar("COUCHBASE_TYPE")
    if err != nil {
        return Config{}, err
    }

    return Config{
        username:   username,
        password:   password,
        host:       host,
        tls:        strings.ToLower(tlsStr) == "true",
        bucketName: bucketName,
        cType:      cType,
    }, nil
}

func app() error {
    config, err := loadConfig()
    if err != nil {
        return err
    }

    dataStructureSpec := map[string][]string{
        "_default": {"items"},
    }

    clusterController := controllers.NewClusterController(
        config.host, 
        config.username, 
        config.password, 
        config.tls, 
        config.cType,
    )
    
    if config.cType == "server" {
        if err := clusterController.EnsureInitialized(); err != nil {
            return fmt.Errorf("failed to initialize cluster: %v", err)
        }
    }

    clusterConn, err := clusterController.ConnectWithRetry()
    if err != nil {
        return fmt.Errorf("failed to connect to cluster: %v", err)
    }
    defer clusterConn.Close()

    bucketController := controllers.NewBucketController(clusterController, clusterConn)
    bucket, err := bucketController.EnsureCreated(config.bucketName, 100)
    if err != nil {
        return fmt.Errorf("failed to ensure bucket exists: %v", err)
    }

    dataStructureController := controllers.NewDataStructureController(bucket)
    if err := dataStructureController.Create(dataStructureSpec); err != nil {
        return fmt.Errorf("failed to create data structures: %v", err)
    }

    return nil
}

func main() {
    if err := app(); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }
}
