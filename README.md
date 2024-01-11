# Lethal Company Manager

Your mod updater of confidence. Gets the mods from thundermods.

### Requirements: 

- VPS / Server.
- Some cron/crontab knowledge.
- Some web server knowledge.
- At least 1 neuron.

### How to set up the server.

1. Install requirements.txt (pip install -r requirements.txt)
2. Download server.py on your server.
3. Change the upload_path variable inside the server file to your own web server path. (Apache/NGINX)
4. Create a cron job that runs the server file with your desired time, remember, don't do it too often or you might get ratelimited.
5. Enjoy.

### How to set up the client.

1. Install requirements.txt (pip install -r requirements.txt)
2. Run the file.
