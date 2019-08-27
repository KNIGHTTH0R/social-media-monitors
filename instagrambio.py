import requests
import json
from dhooks import Webhook, Embed
import time
from bs4 import BeautifulSoup

#cd C:\Users\hugom\Desktop\suprattle code\client-code\a-notify && python instagrambio.py

start = input("Input Anything To Start: ")
instagramUsername = input("Instagran Username: ")
print("Monitor Started")
discordWebhook = "https://discordapp.com/api/webhooks/615628524535021578/vvRNmWxGBnRV5bIHJ9VdZAN5iEjB5rQGz90fxXXEm_FFCO6lRCWukOgnH2ZbpIkd7d6X"

while True:
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
    # This is all the profile data
    scriptJson = json.loads(scriptJsonSrc)
    print("Checking")
    instagramBio = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['biography']
    instagramBioUrl = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']
    instagramName = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
    instagramFollowers = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
    instagramFollowing = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count']
    instagramProfileImage = scriptJson['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']
    # now we check these values against the previous checks values, it should throw an error the first time
    try:
        if instagramBio != oldInstagramBio:
            print("Detected Change in Bio")
            print("Sending Webhook")
            changeType = "Bio Text"
            hook = Webhook(discordWebhook)
            embed = Embed(
            description="{} Change".format(changeType),
            color=11075584,
            timestamp='now',
            )
            embed.add_field(name='Link', value="{}".format(instagramUrl), inline=True) 
            embed.add_field(name='Old Bio/New Bio', value="{}/{}".format(oldInstagramBio, instagramBio), inline=False) 
            embed.set_author(name='Notify - Instagran Moniotr')
            embed.set_footer(text='Notify | @suprattle')
            try:
                embed.set_thumbnail(instagramProfileImage)
                hook.send(embed=embed)
            except:
                hook.send(embed=embed)
        ignorer = "20"
        if instagramBioUrl != oldInstagramBioUrl:
            print("Detected Change in Bio Url")
            print("Sending Webhook")
            changeType = "Bio Url"
            hook = Webhook(discordWebhook)
            embed = Embed(
            description="{} Change".format(changeType),
            color=11075584,
            timestamp='now',
            )
            embed.add_field(name='Link', value="{}".format(instagramUrl), inline=True) 
            embed.add_field(name='Old Bio Url/New Bio Url', value="{}/{}".format(oldInstagramBioUrl, instagramBioUrl), inline=False) 
            embed.set_author(name='Notify - Instagran Moniotr')
            embed.set_footer(text='Notify | @suprattle')
            try:
                embed.set_thumbnail(instagramProfileImage)
                hook.send(embed=embed)
            except:
                hook.send(embed=embed)
        ignorer = "20"
        if instagramName != oldInstagramName:
            print("Detected Change in Name")
            print("Sending Webhook")
            changeType = "Name"
            hook = Webhook(discordWebhook)
            embed = Embed(
            description="{} Change".format(changeType),
            color=11075584,
            timestamp='now',
            )
            embed.add_field(name='Link', value="{}".format(instagramUrl), inline=True) 
            embed.add_field(name='Old Name/New Name', value="{}/{}".format(oldInstagramName, instagramName), inline=False) 
            embed.set_author(name='Notify - Instagran Moniotr')
            embed.set_footer(text='Notify | @suprattle')
            try:
                embed.set_thumbnail(instagramProfileImage)
                hook.send(embed=embed)
            except:
                hook.send(embed=embed)
        ignorer = "20"
        if int(instagramFollowing) > int(oldInstagramFollowing):
            print("Detected Change in Following")
            print("Sending Webhook")
            changeType = "Following"
            hook = Webhook(discordWebhook)
            embed = Embed(
            description="{} Change".format(changeType),
            color=11075584,
            timestamp='now',
            )
            embed.add_field(name='Link', value="{}".format(instagramUrl), inline=True) 
            embed.add_field(name='Old Following Number/New Following Number', value="{}/{}".format(str(instagramFollowing), str(oldInstagramFollowing)), inline=False) 
            embed.set_author(name='Notify - Instagran Moniotr')
            embed.set_footer(text='Notify | @suprattle')
            try:
                embed.set_thumbnail(instagramProfileImage)
                hook.send(embed=embed)
            except:
                hook.send(embed=embed)
        oldInstagramBio = instagramBio
        oldInstagramBioUrl = instagramBioUrl
        oldInstagramName = instagramName
        oldInstagramFollowers = instagramFollowers
        oldInstagramFollowing = instagramFollowing 
        oldInstagramProfileImage = instagramProfileImage
        time.sleep(3)
    except Exception as e:
        oldInstagramBio = instagramBio
        oldInstagramBioUrl = instagramBioUrl
        oldInstagramName = instagramName
        oldInstagramFollowers = instagramFollowers
        oldInstagramFollowing = instagramFollowing 
        oldInstagramProfileImage = instagramProfileImage
        print("Hit Error - " + str(e))
        time.sleep(3)
                

