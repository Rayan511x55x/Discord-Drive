# 📁 Discord Drive

**Discord Drive** is a lightweight tool that turns a Discord channel into a cloud storage system. It allows you to **upload**, **view**, **download**, **rename**, and **delete** files through a sleek web interface.

> 🛠️ Created by **RPP**

---

## 🚀 Features

- 📤 Upload files up to **25MB**
- 📄 Display stored files in a beautiful table
- ⏬ Download files directly from Discord CDN
- ✏️ Rename uploaded files
- ❌ Delete files from the channel
- 🔁 Auto-refresh file list every 10 seconds
- 🎨 Modern dark-themed UI

---

## ⚙️ Installation

### 🧰 Requirements

- Python 3.8+
- A Discord account
- A Discord bot with the following permissions **in one channel**:
  - Read Messages
  - Read Message History
  - Send Messages
  - Attach Files
  - Delete Messages

---

### 🧑‍💻 1. Clone the project

```bash
git clone https://github.com/yourusername/discord-drive.git
cd discord-drive
```

---

🐍 2. Install dependencies

pip install -r requirements.txt

Or manually:

pip install flask flask-cors discord.py


---

🔧 3. Configure the bot

Open the Python file (e.g. main.py) and set the following:

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID  # e.g. 123456789012345678


---

▶️ 4. Run the bot and server

python main.py

It will:

Start a Flask server on http://localhost:5000

Log your bot into Discord

Listen for upload, rename, delete, and file fetch requests



---

🌐 5. Open the front-end

Open the index.html file in your browser.

You’ll be able to:

Upload files to the Discord channel

See all uploaded files (name, type, time)

Download files

Rename or delete them


> The file list auto-refreshes every 10 seconds.




---

🛡️ Notes

Files are stored in the configured Discord channel.

This is a great lightweight "Drive"-like tool using Discord as a database.

Ideal for limited personal or team storage use.



---

### ❤️ Credits

Created with care by RPP
