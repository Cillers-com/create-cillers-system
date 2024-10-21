package main

import (
    "bufio"
    "fmt"
    "io/ioutil"
    "os"
    "path/filepath"
    "sort"
    "strings"
)

func main() {
    ignore_patterns := read_ignore_file()
    current_dir, err := os.Getwd()
    if err != nil {
        fmt.Println("Error getting current directory:", err)
        return
    }

    file_contents := make(map[string]string)
    err = filepath.Walk(current_dir, func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        rel_path, _ := filepath.Rel(current_dir, path)
        if should_ignore(rel_path, ignore_patterns) {
            if info.IsDir() {
                return filepath.SkipDir
            }
            return nil
        }
        if !info.IsDir() {
            content, err := ioutil.ReadFile(path)
            if err != nil {
                return err
            }
            file_contents[rel_path] = string(content)
        }
        return nil
    })

    if err != nil {
        fmt.Println("Error walking the directory tree:", err)
        return
    }

    print_sorted_file_contents(file_contents, current_dir)
}

func read_ignore_file() []string {
    ignore_file := ".cillers/ai/ignore"
    patterns := []string{ignore_file}

    file, err := os.Open(ignore_file)
    if err != nil {
        return patterns
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        patterns = append(patterns, strings.TrimSpace(scanner.Text()))
    }

    return patterns
}

func should_ignore(path string, ignore_patterns []string) bool {
    for _, pattern := range ignore_patterns {
        if glob_match(pattern, path) {
            return true
        }
    }
    return false
}

func glob_match(pattern, path string) bool {
    parts := strings.Split(pattern, "**")
    if len(parts) == 1 {
        matched, _ := filepath.Match(pattern, path)
        return matched
    }

    if !strings.HasPrefix(path, parts[0]) {
        return false
    }

    path = path[len(parts[0]):]
    for i := 1; i < len(parts)-1; i++ {
        idx := strings.Index(path, parts[i])
        if idx == -1 {
            return false
        }
        path = path[idx+len(parts[i]):]
    }

    return strings.HasSuffix(path, parts[len(parts)-1])
}

func print_sorted_file_contents(file_contents map[string]string, current_dir string) {
    var current_dir_files, other_files []string

    for path := range file_contents {
        if filepath.Dir(path) == "." {
            current_dir_files = append(current_dir_files, path)
        } else {
            other_files = append(other_files, path)
        }
    }

    sort.Strings(current_dir_files)
    sort.Strings(other_files)

    all_files := append(current_dir_files, other_files...)

    for _, path := range all_files {
        fmt.Printf("%s:\n%s\n\n", path, file_contents[path])
    }
}
