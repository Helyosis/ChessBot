# ChessBot
ChessBot is a bot made for discord using discord.py library. It can be used to play chess with your friends.
You can host it on your own server/computer and add new pieces easily without breaking anything

# How to use this bot ?
1. Create a new application on Discord's Developper portal and create a new bot.
    Copy it's token, and save the application id for later.
2. Clone the repository and create a new file "creds.txt". On the first line, paste your token, there should be no trailing space.
3. Run bot.py using python 3.6+
4. Invite your bot in your server by clicking on this link and changing APPLICATION_ID by your application id saved earlier.
    https://discordapp.com/oauth2/authorize?client_id=APPLICATION_ID&scope=bot&permissions=35856
5. Go on your server and type **!chess start @someone** and replacing @someone by the mention of your desired enemy.

# Usages
To move a piece, you have to specify the square of origin, and the square of destination.

*Example: If I want to go from a2 to a4 with my pawn, I'll have to send* **a2 a4**

To castle, the origin square is the king and the destination is the rook you want to castle with 
