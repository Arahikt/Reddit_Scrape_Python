from tkinter import scrolledtext

import praw
from datetime import datetime
from tkinter import *

from prawcore import NotFound, ResponseException


def searchSubredditExists(subreddit):
    try:
        reddit = praw.Reddit('reddit-configuration-bot1')
        # reddit.subreddit(subreddit)
        reddit.subreddits.search_by_name(subreddit)

        return True
    except NotFound:
        return False
    except ResponseException:
        return False


def searchKeywordWindow():

    editor = Tk()
    editor.title('Search keyword in Subreddit')
    editor.geometry("530x500")

    searchTermLabel = Label(editor, text="Search Term:")
    searchTermLabel.grid(row=0, column=0,  pady=15,)
    searchTermEntry = Entry(editor, width=25, borderwidth=5)
    searchTermEntry.grid(row=0, column=1 )
    searchTermEntry.insert(0, "")

    subredditLabel = Label(editor, text="Subreddit To Search:")
    subredditLabel.grid(row=3, column=0,  pady=15,)
    subredditEntry = Entry(editor, width=25, borderwidth=5)
    subredditEntry.grid(row=3, column=1)
    subredditEntry.insert(0, "")

    subredditExistsLabel = Label(editor, text="")
    subredditExistsLabel.grid(row=4, column=0, sticky=E)
    text_area_frame = Frame(editor)
    text_area_frame.grid(row=6, column=0, columnspan=2)
    text_area = scrolledtext.ScrolledText(text_area_frame, width=60, height=19, bg="Alice blue")
    text_area.grid(row=0, column=0, pady=15, padx=15)

    def executeSubredditTracking():
        if (len(subredditEntry.get()) > 0):

            subredditExists = searchSubredditExists(str(subredditEntry.get()))

            if (subredditExists == False):
                subredditExistsLabel.configure(text="Subreddit not found.    ", fg="#AEB6BF")
                return False
            else:
                subredditExistsLabel.configure(text="Subreddit exists.    ", fg="#AEB6BF")
                return True

        else:
            subredditExistsLabel.configure(text="Please Enter Subreddit.", fg="#AEB6BF")

    def fill():
        text_area.delete('1.0', END)
        userExists=executeSubredditTracking()

        if userExists==True:
            if (len(subredditEntry.get()) > 0) and (len(searchTermEntry.get()) > 0):

                reddit = praw.Reddit('reddit-configuration-bot1')
                subreddit = reddit.subreddit(subredditEntry.get())

                subreddit = subreddit.search(searchTermEntry.get(), limit=50)
                counter = 1
                if subreddit:
                    text_area.insert(INSERT, "Targeted Subreddit:  " + str(subredditEntry.get()) + "\n\n")
                    text_area.insert(INSERT, "Search Term:  " + searchTermEntry.get() + "\n\n\n *********************\n")

                    for submission in subreddit:
                        text_area.insert(INSERT, counter)
                        text_area.insert(INSERT, "\nID:  \n" + submission.id + "\n")
                        text_area.insert(INSERT, "\nTitle:  \n" + submission.title + "\n")
                        text_area.insert(INSERT, "\nScore:  \n" + str(submission.score) + "\n")
                        text_area.insert(INSERT, "\nURL:  \n" + submission.url + "\n")
                        text_area.insert(INSERT, "\nTime:  \n" + str(datetime.fromtimestamp(submission.created_utc)) + "\n"+ "\n *********************\n")
                        counter +=1
                    text_area.configure(state="disabled")

    searchButtonSubreddit = Button(editor, text="Search Subreddit", command=fill)
    searchButtonSubreddit.grid(row=5, column=1, sticky=W)


