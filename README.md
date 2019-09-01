# emotes-when-sub
Spam emotes when a user subs a to a twitch channel

# How to get started
You would need [Python 3.6.X](https://www.python.org/downloads/) or later.

# External Libraries 
* [Colorama](https://pypi.org/project/colorama/)
___
`pip install [Library]`
___
**Replace "Library" above with the one you are installing**

## Client Id (CID): 
* Go to [Twitch Dev Website](https://glass.twitch.tv/console/apps/create)
* Name your application!
* Set **OAuth Redirect** URL to `http://localhost`
* Set **Category** to **Analytics Tool**
* Now in the Developer Applications page, click **Manage** on the application you now made.
* Now copy the **Client ID** 
* Replace the **client_id** on Line 19 with the new one

## OAUTH:
* Go to [Twitch Apps Website](https://twitchapps.com/tmi/)

# How to Run
___
Now run the line `python EWS.py`
___
# License
This project is licensed under GNU General Public License 

