import requests
import json
from dhooks import Webhook, Embed
import time
from bs4 import BeautifulSoup

start = input("Input Anything To Start: ")
instagramUsername = input("Instagran Username: ")
if "@" in instagramUsername:
    instagramUsername = instagramUsername.replace("@", "")
retryDelay = input("Monitor Delay: ")
print("Monitor Started")
discordWebhook = "" #put your webhook in the quotes

def webhook(discordWebhook, instagramUrl, newValue, changeType, instagramUsername):
    try:
        hook = Webhook(discordWebhook)
        embed = Embed(
        description=f"{changeType} Change - @{instagramUsername}",
        color=0XFFA574,
        timestamp='now',
        )
        embed.add_field(name='Profile Link', value=instagramUrl, inline=True) 
        embed.add_field(name='New Update', value=newValue, inline=False) 
        embed.set_author(name='Instagran Monitor')
        embed.set_footer(text='@suprattle')
        try:
            embed.set_thumbnail(instagramProfileImage)
            hook.send(embed=embed)
        except:
            hook.send(embed=embed)
    except:
        pass

def webhook_post(discordWebhook, instagramUrl, postCaption, postImage, instagramUsername):
    try:
        hook = Webhook(discordWebhook)
        embed = Embed(
        description="New Post ",
        color=0XFFA574,
        timestamp='now',
        )
        embed.add_field(name='Profile Link', value=str(instagramUrl), inline=True) 
        embed.add_field(name='Post Caption', value=str(postCaption), inline=False) 
        embed.set_author(name='Instagran Monitor')
        embed.set_footer(text='@suprattle')
        embed.set_image(str(postImage))
        hook.send(embed=embed)
    except:
        pass


# task code

while True:
    try:
        instagramUrl = "https://www.instagram.com/" + instagramUsername
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        r = requests.get(instagramUrl, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        scriptJsonSrc = soup.find_all("script")
        scriptJsonSrc = scriptJsonSrc[4]
        scriptJsonSrc = scriptJsonSrc.get_text()
        scriptJsonSrc = scriptJsonSrc.split("window._sharedData = ")
        scriptJsonSrc = scriptJsonSrc[1]
        scriptJsonSrc = str(scriptJsonSrc)
        scriptJsonSrc = scriptJsonSrc.replace(";", "")
        scriptJson = json.loads(scriptJsonSrc)

        print("Checking")
        #remove the line above to remove console spam

        instagramBio = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['biography']
        instagramBioUrl = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']
        instagramName = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
        instagramFollowers = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
        instagramFollowing = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count']
        instagramProfileImage = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']
        userId = instagramProfileImage = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']["id"]
        recentPostSrc = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]

        # now we check these values against the previous checks values, it should throw an error the first time

        try:
            if recentPostSrc != oldRecentPostSrc:
                recentPostCaption = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                webhook_post(discordWebhook, instagramUrl, recentPostCaption, recentPostSrc, instagramUsername)
            if instagramBio != oldInstagramBio:
                print("Detected Change in Bio")
                print("Sending Webhook")
                changeType = "Bio Text"
                newValue = instagramBio
                webhook(discordWebhook, instagramUrl, newValue, changeType, instagramUsername)
            if instagramBioUrl != oldInstagramBioUrl:
                print("Detected Change in Bio Url")
                print("Sending Webhook")
                changeType = "Bio Url"
                newValue = instagramBioUrl
                webhook(discordWebhook, instagramUrl, newValue, changeType, instagramUsername)
            if instagramName != oldInstagramName:
                print("Detected Change in Name")
                print("Sending Webhook")
                changeType = "Name"
                newValue = instagramName
                webhook(discordWebhook, instagramUrl, newValue, changeType, instagramUsername)
            if int(instagramFollowing) > int(oldInstagramFollowing):
                print("Detected Change in Following")
                print("Sending Webhook")
                changeType = "Following"
                newValue = str(instagramFollowing)
                webhook(discordWebhook, instagramUrl, newValue, changeType, instagramUsername)
            oldInstagramBio = instagramBio
            oldInstagramBioUrl = instagramBioUrl
            oldInstagramName = instagramName
            oldInstagramFollowers = instagramFollowers
            oldInstagramFollowing = instagramFollowing 
            oldInstagramProfileImage = instagramProfileImage
            oldRecentPostSrc = recentPostSrc
            time.sleep(int(retryDelay))
        except Exception as e:
            oldInstagramBio = instagramBio
            oldInstagramBioUrl = instagramBioUrl
            oldInstagramName = instagramName
            oldInstagramFollowers = instagramFollowers
            oldInstagramFollowing = instagramFollowing 
            oldInstagramProfileImage = instagramProfileImage
            oldRecentPostSrc = recentPostSrc
            print("Hit Error - " + str(e))
            try:
                time.sleep(int(retryDelay))
            except:
                print("Invalid Retry Delay -> Using 3 Seconds")
                time.sleep(3)
    except:
        try:
            print("Error - " + str(e))
            time.sleep(int(retryDelay))
        except:
            print("Error - " + str(e))
            time.sleep(3)
