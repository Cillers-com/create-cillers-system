package controllers

import (
    "fmt"

    "github.com/couchbase/gocb/v2"
)

type DataStructureController struct {
    bucket *gocb.Bucket
}

func NewDataStructureController(bucket *gocb.Bucket) *DataStructureController {
    return &DataStructureController{
        bucket: bucket,
    }
}

func (c *DataStructureController) createScope(collectionMgr *gocb.CollectionManager, scopeName string) error {
    err := collectionMgr.CreateScope(scopeName, nil)
    if err != nil {
        if gocb.IsErrorScopeExists(err) {
            fmt.Printf("Scope '%s' already exists.\n", scopeName)
            return nil
        }
        return fmt.Errorf("failed to create scope '%s': %v", scopeName, err)
    }
    fmt.Printf("Scope '%s' created successfully.\n", scopeName)
    return nil
}

func (c *DataStructureController) createCollections(collectionMgr *gocb.CollectionManager, scopeName string, collectionNames []string) error {
    for _, collectionName := range collectionNames {
        err := collectionMgr.CreateCollection(gocb.CollectionSpec{
            Name:      collectionName,
            ScopeName: scopeName,
        }, nil)
        if err != nil {
            if gocb.IsErrorCollectionExists(err) {
                fmt.Printf("Collection '%s' already exists in scope '%s'.\n", collectionName, scopeName)
                continue
            }
            return fmt.Errorf("failed to create collection '%s' in scope '%s': %v", collectionName, scopeName, err)
        }
        fmt.Printf("Collection '%s' created successfully in scope '%s'.\n", collectionName, scopeName)
    }
    return nil
}

func (c *DataStructureController) Create(spec map[string][]string) error {
    collectionMgr := c.bucket.Collections()
    
    for scopeName, collectionNames := range spec {
        if scopeName != "_default" {
            if err := c.createScope(collectionMgr, scopeName); err != nil {
                return err
            }
        }
        if err := c.createCollections(collectionMgr, scopeName, collectionNames); err != nil {
            return err
        }
    }
    return nil
}
