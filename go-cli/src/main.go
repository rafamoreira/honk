package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/adrg/xdg"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

type credentials struct {
	ApiCredentials string `json:"api_credentials"`
}
type honk struct {
	Id        int       `json:"id"`
	Honker    string    `json:"honker"`
	Clown     string    `json:"clown"`
	ClownUrl  string    `json:"clown_url"`
	CreatedAt time.Time `json:"created_at"`
}

func getCredentials() credentials {
	var configHome = xdg.ConfigHome
	if configHome == "" {
		configHome := xdg.Home
		configHome += "/.config"
	}
	configDir := filepath.Join(configHome, "/honk")
	err := os.MkdirAll(configDir, os.ModePerm)
	if err != nil {
		log.Fatal(err)
	}
	configFile := configDir + "/config.json"
	f, err := os.ReadFile(configFile)
	var credStruct = credentials{}
	if err != nil {
		var input string
		//log.Println(err)
		if errors.Is(err, os.ErrNotExist) {
			fmt.Println("Configuration not found.")
			fmt.Println("Please paste your api credentials: ")
			_, err2 := fmt.Scan(&input)
			if err2 != nil {
				log.Fatal(err2)
			}

			credStruct.ApiCredentials = input

			file, _ := json.MarshalIndent(credStruct, "", "")
			err3 := os.WriteFile(configFile, file, 0644)
			if err3 != nil {
				log.Fatal(err3)
			}
		}
	} else {
		err = json.Unmarshal(f, &credStruct)
		if err != nil {
			log.Fatal(err)
		}
	}

	return credStruct
}

func getHonks(token string) []byte {
	url := "https://honk.rafaelmc.net/api/honks"
	method := "GET"

	client := &http.Client{}
	req, err := http.NewRequest(method, url, nil)

	if err != nil {
		fmt.Println(err)
	}
	req.Header.Add("Authorization", "Token "+token)

	res, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer func(Body io.ReadCloser) {
		err2 := Body.Close()
		if err2 != nil {
			log.Fatal(err2)
		}
	}(res.Body)

	body, err := io.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}
	//fmt.Println(string(body))
	return body
}

func main() {
	var credentials = getCredentials()
	//log.Println(credentials)
	var body = getHonks(credentials.ApiCredentials)
	var honks []honk
	err := json.Unmarshal(body, &honks)
	if err != nil {
		return
	}
	fmt.Printf("You have %d new honks", len(honks))
}
