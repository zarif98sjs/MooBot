import sys

from moodle_scrapper import *
from bs4 import BeautifulSoup
from requests import session
import requests

import discord
import asyncio
import os

STUDENT_ID = "YOUR_STUDENT_ID"
LOGIN_PASSWORD = "YOUR_LOGIN_PASSWORD"
CHANNEL_ID = "YOUR_CHANNEL_ID"

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID) # channel ID goes here

        count = 0

        while not self.is_closed():

          count+=1
          print("Count :",count)

          '''
          FORUMS
          '''
          print("getiing Old Forum Links ... \n")
          old_forum_links = get_old_forum_links(course_dict)
          # print(old_forum_links)

          print("getiing New Forum Posts ... \n")
          new_forum_posts = get_new_forum_posts(course_dict,old_forum_links,session)
          # print(new_forum_posts)

          '''
          ACTIVITY
          '''
          print("getiing Old Activity Links ... \n")
          old_activity_links = get_old_activity_links(course_dict)
          # print(old_forum_links)

          print("getiing New Activity Posts ... \n")
          new_activity_posts = get_new_activity_posts(course_dict,old_activity_links,session)
          # print(new_activity_posts)

          ## for testing only
          for c_name,post_ara in new_forum_posts.items():
            
            if(len(post_ara)==0):
              continue

            for p in post_ara:
              print(p)
              embedVar = discord.Embed(title="Forum Post ( " +c_name+" ) :rotating_light: ", description=p.title, color=0xb331bd)
              embedVar.add_field(name="Link :paperclips: ", value=p.link, inline=False)
              embedVar.add_field(name="Teacher :person_fencing: ", value="`"+p.author+"`", inline=False)
              await channel.send(embed=embedVar)
              await asyncio.sleep(30) ## 30 seconds

          for c_name,post_ara in new_activity_posts.items():
            
            if(len(post_ara)==0):
              continue

            for p in post_ara:
              print(p)
              embedVar = discord.Embed(title="New Activity ( " + c_name +  " ) :boom: ", description=p.title, color=0xfc9803)
              embedVar.add_field(name="Link :paperclips: ", value=p.link, inline=False)
              await channel.send(embed=embedVar)
              await asyncio.sleep(30) ## 30 seconds


          await asyncio.sleep(20*60) ## check after 20 minutes 

if __name__ == "__main__":

  #logging in
  print("logging in...\n")
  session = login(STUDENT_ID, LOGIN_PASSWORD)

  #get courses
  print("getting Courses...\n")
  course_dict = getCourses(session)
  print(course_dict)

  client = MyClient()
  client.run(os.getenv('TOKEN'))