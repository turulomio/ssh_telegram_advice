# SSH Telegram Advice
Logs in telegram ssh logins

## To install you need
- Create a new bot in your Telegram Account
- Create a Telegram group to send messages to (With the bot as a user)
- You need to get chat_id of the group (Sending a message). Look into  https://api.telegram/.org/bot__/getUpdates
- Configure /etc/ssh_telegram_advice/ssh_telegram_advice, using default template

## Changelog
### 0.2.0 (2022-04-28)
- Messages are now send in groups of 3, when needed.

### 0.1.1 (2022-04-25)
- Fixed error in distribution

### 0.1.0 (2022-04-25)
- First and fast version, but works
