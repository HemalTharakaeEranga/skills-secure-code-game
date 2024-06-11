// Welcome to Secure Code Game Season-2/Level-2!

// Follow the instructions below to get started:

// 1. code_test.go is passing but the code is vulnerable
// 2. Review the code. Can you spot the bugs(s)?
// 3. Fix the code.go, but ensure that code_test.go passes
// 4. Run hack_test.go and if passing then CONGRATS!
// 5. If stuck then read the hint
// 6. Compare your solution with solution/solution.go

package main

import (
	"encoding/json"
	"log"
	"net/http"
	"regexp"
)

var reqBody struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

func isValidEmail(email string) bool {
	// The provided regular expression pattern for email validation by OWASP
	// https://owasp.org/www-community/OWASP_Validation_Regex_Repository
	emailPattern := `^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$`
	match, err := regexp.MatchString(emailPattern, email)
	if err != nil || !match {
		return false
	}
	return true
}

func loginHandler(w http.ResponseWriter, r *http.Request) {

	var testFakeMockUsers = map[string]string{
		"user1@example.com": "password12345",
		"user2@example.com": "B7rx9OkWVdx13$QF6Imq",
		"user3@example.com": "hoxnNT4g&ER0&9Nz0pLO",
		"user4@example.com": "Log4Fun",
	}

	if r.Method != "POST" {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	decode := json.NewDecoder(r.Body)
	decode.DisallowUnknownFields()

	if err := decode.Decode(&reqBody); err != nil {
		http.Error(w, "Cannot decode body", http.StatusBadRequest)
		return
	}

	if !isValidEmail(reqBody.Email) {
		http.Error(w, "Invalid email format", http.StatusBadRequest)
		return
	}

	storedPassword, ok := testFakeMockUsers[reqBody.Email]
	if !ok {
		http.Error(w, "Invalid Email or Password", http.StatusUnauthorized)
		return
	}

	if reqBody.Password != storedPassword {
		http.Error(w, "Invalid Email or Password", http.StatusUnauthorized)
		return
	}

	// Log a generic message without sensitive information
	log.Printf("Successful login request")
	w.WriteHeader(http.StatusOK)
}

func main() {
	http.HandleFunc("/login", loginHandler)
	log.Print("Server started. Listening on :8081")
	err := http.ListenAndServe(":8081", nil)
	if err != nil {
		log.Fatalf("HTTP server ListenAndServe: %q", err)
	}
}



