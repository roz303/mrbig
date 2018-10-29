package main
import (
	"bufio"
	"strings"
	"strconv"
	"time"
        "log"
        "os"
	"fmt"
        "github.com/yanzay/tbot"
)

var database map[string]string
var days int
var path string
var layout string
func main() {
	database = make(map[string]string)
	path = "/path/to/telegram/user/list"
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		user := scanner.Text()
		database[user] = "?"
	}
	layout = "2006-01-02"
	fmt.Println("User database updated and ready.")
	bot, err := tbot.NewServer("YOUR TELEGRAM AUTH TOKEN")
        if err != nil {
                log.Fatal(err)
        }
	fmt.Println("Mr.Big is online.")
        bot.Handle("/answer", "42")
	bot.HandleDefault(logger)
        bot.ListenAndServe()
}

func logger(message *tbot.Message) {
	input := strings.ToUpper(message.Text())
	if(strings.Contains(input, "LURK ")){
		s := strings.Split(message.Text(), " ")
		amount := s[1]
		getLurkers(message, amount)
	}
	user := message.From.UserName
	whenPosted := time.Now().Local().Format(layout)
	database[user] = whenPosted
	fmt.Println("Logged: " + message.Text() + "\nFrom: " + user + "\nAt: " + whenPosted)
	//message.Reply(output)
}
func getLurkers(message *tbot.Message, amt string){
	now := time.Now()
	output := "You requested those who have lurked for " + amt + " days.\n"
	days, err := strconv.Atoi(amt)
	if(err != nil){
		message.Reply("Format: lurk [number of days]")
		return
	}

	output = output + "Lurkers in the past " + amt + " days as of " + time.Now().Local().Format(layout) + ":\n"
	message.Reply(output)
	output = ""
	for k, v := range database {
		if(v == "?") {
		output  = output + "User: " + k + "\nLast active: " + v + "\n"
		} else {
			usertime, err := time.Parse(layout, v)
			if(err != nil) {
				message.Reply("FATAL ERROR IN TIME")
			}
			selectedTime := now.AddDate(0,0,-days)
			if(usertime.Before(selectedTime)){
			output = output + "User: " + k + "\nLastActive: " + v + "\n"
			}
		}
	} 
	message.Reply(output)
}
