package controllers

import (
    "fmt"
    "time"

    "github.com/couchbase/gocb/v2"
)

type Controller struct {
    clusterController interface{
        GetType() string
    }
    cluster *gocb.Cluster
}

func NewBucketController(clusterController interface{ GetType() string }, cluster *gocb.Cluster) *Controller {
    return &Controller{
        clusterController: clusterController,
        cluster:          cluster,
    }
}

func (c *Controller) EnsureCreated(bucketName string, ramQuotaMB uint64) (*gocb.Bucket, error) {
    bucketMgr := c.cluster.Buckets()
    
    _, err := bucketMgr.GetBucket(bucketName, nil)
    if err == nil {
        fmt.Printf("Bucket '%s' already exists.\n", bucketName)
        return c.waitForBucketReady(bucketName)
    }

    if c.clusterController.GetType() == "capella" {
        return nil, fmt.Errorf("no bucket '%s' exists in Capella cluster. Bucket must be created manually using the Capella UI", bucketName)
    }

    err = bucketMgr.CreateBucket(gocb.CreateBucketSettings{
        Name:        bucketName,
        BucketType: gocb.CouchbaseBucketType,
        RAMQuotaMB: ramQuotaMB,
    }, nil)
    if err != nil {
        return nil, fmt.Errorf("failed to create bucket '%s': %v", bucketName, err)
    }

    fmt.Printf("Bucket '%s' created successfully.\n", bucketName)
    return c.waitForBucketReady(bucketName)
}

func (c *Controller) waitForBucketReady(bucketName string) (*gocb.Bucket, error) {
    maxRetries := 30
    retryInterval := time.Second

    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        bucket := c.cluster.Bucket(bucketName)
        err := bucket.Ping(nil)
        if err == nil {
            fmt.Printf("Bucket '%s' is ready.\n", bucketName)
            return bucket, nil
        }
        lastErr = err
        
        if attempt == maxRetries-1 {
            fmt.Println("Timeout: waiting until bucket ready.")
            return nil, lastErr
        }
        
        fmt.Printf("Waiting until bucket '%s' is ready\n", bucketName)
        time.Sleep(retryInterval)
    }
    return nil, lastErr
}
