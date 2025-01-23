package controllers

import (
    "fmt"
    "io"
    "net/http"
    "net/url"
    "strings"
    "time"

    "github.com/couchbase/gocb/v2"
)

type ClusterController struct {
    host     string
    username string
    password string
    tls      bool
    cType    string
}

func NewClusterController(host, username, password string, tls bool, cType string) *ClusterController {
    return &ClusterController{
        host:     host,
        username: username,
        password: password,
        tls:      tls,
        cType:    cType,
    }
}

func (c *ClusterController) GetType() string {
    return c.cType
}

func (c *ClusterController) getConnectionString() string {
    protocol := "couchbases"
    if !c.tls {
        protocol = "couchbase"
    }
    return fmt.Sprintf("%s://%s", protocol, c.host)
}

func (c *ClusterController) getClusterInitParams() (string, url.Values) {
    protocol := "https"
    port := "18091"
    if !c.tls {
        protocol = "http"
        port = "8091"
    }

    initURL := fmt.Sprintf("%s://%s:%s/clusterInit", protocol, c.host, port)
    data := url.Values{
        "username":            {c.username},
        "password":            {c.password},
        "services":            {"kv,n1ql,index,fts,eventing"},
        "hostname":            {"127.0.0.1"},
        "memoryQuota":         {"256"},
        "sendStats":           {"false"},
        "clusterName":         {"cillers"},
        "setDefaultMemQuotas": {"true"},
        "indexerStorageMode":  {"plasma"},
        "port":               {"SAME"},
    }
    return initURL, data
}

func (c *ClusterController) EnsureInitialized() error {
    initURL, data := c.getClusterInitParams()
    
    maxRetries := 100
    for attempt := 0; attempt < maxRetries; attempt++ {
        resp, err := http.PostForm(initURL, data)
        if err != nil {
            if attempt == maxRetries-1 {
                return fmt.Errorf("timeout: waiting until cluster is started: %v", err)
            }
            fmt.Println("Waiting until cluster is started ...")
            time.Sleep(time.Second)
            continue
        }
        defer resp.Body.Close()

        body, err := io.ReadAll(resp.Body)
        if err != nil {
            return fmt.Errorf("failed to read response body: %v", err)
        }

        responseStr := string(body)
        if strings.Contains(responseStr, "already initialized") || strings.Contains(responseStr, "Unauthorized") {
            fmt.Println("Cluster already initialized.")
            return nil
        }

        fmt.Println(responseStr)
        fmt.Println("Cluster initialization successful.")
        return nil
    }
    return fmt.Errorf("failed to initialize cluster after maximum retries")
}

func (c *ClusterController) Connect() (*gocb.Cluster, error) {
    opts := gocb.ClusterOptions{
        Authenticator: gocb.PasswordAuthenticator{
            Username: c.username,
            Password: c.password,
        },
    }
    if c.tls {
        opts.SecurityConfig.TLSSkipVerify = false
    }

    cluster, err := gocb.Connect(c.getConnectionString(), opts)
    if err != nil {
        return nil, fmt.Errorf("failed to connect to cluster: %v", err)
    }

    err = cluster.WaitUntilReady(time.Second*300, nil)
    if err != nil {
        return nil, fmt.Errorf("cluster not ready: %v", err)
    }

    return cluster, nil
}

func (c *ClusterController) ConnectWithRetry() (*gocb.Cluster, error) {
    maxRetries := 30
    retryInterval := time.Second

    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        cluster, err := c.Connect()
        if err == nil {
            return cluster, nil
        }
        lastErr = err

        if attempt == maxRetries-1 {
            return nil, fmt.Errorf("failed to connect after %d attempts: %v", maxRetries, lastErr)
        }

        fmt.Println("Waiting for connection to cluster ...")
        time.Sleep(retryInterval)
    }
    return nil, lastErr
}
