from tkinter import *
import praw
from tkinter import scrolledtext
import prawcore
from prawcore import NotFound, ResponseException
from datetime import *
import initialize


def searchUserExists(username):
    try:
        reddit = praw.Reddit('reddit-configuration-bot1')
        reddit.redditor(username).id
        return True
    except NotFound:
        return False


def searchSubredditExists(subreddit):
    try:
        reddit = praw.Reddit('reddit-configuration-bot1')
        # reddit.subreddit(subreddit)
        reddit.subreddits.search_by_name(subreddit)

        return True
    except NotFound:
        return False


def createNewWindowKeyWordUsage():
    editor = Tk()
    editor.title('Track User Keyword Usage')
    editor.geometry("1000x600")
    reddit = praw.Reddit('reddit-configuration-bot1')
    userToTrackLabel = Label(editor, text="Username to Track").grid(row=0, column=0)
    usertoTrackEntry = Entry(editor, width=30, borderwidth=5)
    usertoTrackEntry.grid(row=0, column=1)
    usertoTrackEntry.insert(0, "")
    userExistLabel = Label(editor, text="")
    userExistLabel.grid(row=1, column=0, sticky=E)

    global i
    i = 3
    listWordBoxes = []

    def prevPage():

        editor.destroy()
        mainloop()

    backButton = Button(editor, text="Previous Page", command=prevPage)
    backButton.grid(row=8, column=0)

    def createNewTextBox(ind):
        keyword = Entry(editor, width=30, borderwidth=5)
        keyword.grid(row=ind, column=1)
        keyword.insert(0, "")
        listWordBoxes.append(keyword)
        global i
        i += 1

    def executeTracking():
        wordsDict = {}
        for w in listWordBoxes:
            wordsDict[str(w.get())] = 0

    def executeUserTracking():
        if (len(usertoTrackEntry.get()) != 0):
            userExists = searchUserExists(str(usertoTrackEntry.get()))
            if (userExists == False):
                userExistLabel.configure(text="User not found.    ", fg="#AEB6BF")
            else:
                userExistLabel.configure(text="User exists.     ", fg="#AEB6BF")
        else:
            userExistLabel.configure(text="Please Enter Username.", fg="#AEB6BF")

    searchButtonUser = Button(editor, text="Search user", command=executeUserTracking)
    searchButtonUser.grid(row=2, column=1, sticky=W)

    buttonKeywordUsage = Button(editor, text="+",
                                command=lambda: createNewTextBox(i)).grid(row=2, column=0)

    buttonExecuteTracking = Button(editor, text="Track Keywords:",
                                   command=executeTracking).grid(row=2, column=5)

    editor.destroy()


def createNewWindowActivityTracking():
    # 2nd Button in main window

    editor = Tk()
    editor.title('Track User Activity')
    editor.geometry("650x750")

    reddit = praw.Reddit('reddit-configuration-bot1')
    userToTrack = Label(editor, text="Username To Track:").grid(row=0, column=0, sticky=E, pady=15, padx=15)
    usertoTrackEntry = Entry(editor, width=35, borderwidth=5)
    usertoTrackEntry.grid(row=0, column=1, sticky=W)
    usertoTrackEntry.insert(0, "")
    userExistLabel = Label(editor, text="")
    userExistLabel.grid(row=1, column=0, sticky=E)
    emptyLabel0 = Label(editor, text="")
    emptyLabel0.grid(row=0, column=3)

    def executeUserTracking():
        if (len(usertoTrackEntry.get()) != 0):
            userExists = searchUserExists(str(usertoTrackEntry.get()))
            if (userExists == False):
                userExistLabel.configure(text="User not found.    ", fg="#AEB6BF")
            else:
                userExistLabel.configure(text="User exists.     ", fg="#AEB6BF")
        else:
            userExistLabel.configure(text="Please Enter Username.", fg="#AEB6BF")

    searchButtonUser = Button(editor, text="Search user", command=executeUserTracking)
    searchButtonUser.grid(row=2, column=1, sticky=W)

    emptyLabel = Label(editor, text="")
    emptyLabel.grid(row=3, column=0)

    subredditLabel = Label(editor, text="Subreddit To Search:")
    subredditLabel.grid(row=3, column=0, sticky=E, pady=15, padx=15)

    subredditTrackEntry = Entry(editor, width=35, borderwidth=5)
    subredditTrackEntry.grid(row=3, column=1, sticky=W)

    subredditTrackEntry.insert(0, "")
    subredditExistsLabel = Label(editor, text="")
    subredditExistsLabel.grid(row=4, column=0, sticky=E)

    def executeSubredditTracking():
        if (len(subredditTrackEntry.get()) > 0):

            subredditExists = searchSubredditExists(str(subredditTrackEntry.get()))

            if (subredditExists == False):
                subredditExistsLabel.configure(text="Subreddit not found.    ", fg="#AEB6BF")
            else:
                subredditExistsLabel.configure(text="Subreddit exists.    ", fg="#AEB6BF")
                subredditExists = True
        else:
            subredditExistsLabel.configure(text="Please Enter Subreddit.", fg="#AEB6BF")

    searchButtonSubreddit = Button(editor, text="Search Subreddit", command=executeSubredditTracking)
    searchButtonSubreddit.grid(row=5, column=1, sticky=W)

    def searchUserWithSubreddit():
        reddit = praw.Reddit('reddit-configuration-bot1')
        text_area.delete('1.0', END)
        if ((len(usertoTrackEntry.get()) != 0) and (len(subredditTrackEntry.get()) != 0)):
            if (userExistLabel.cget("text") == "User exists.     ") & (
                    subredditExistsLabel.cget("text") == "Subreddit exists.    "):
                if (
                        timeframeEntry.get() == "hour" or timeframeEntry.get() == "day" or timeframeEntry.get() == "week" or timeframeEntry.get() == "month" or timeframeEntry.get() == "all"):

                    executeUserTracking()
                    executeSubredditTracking()
                    subreddit = reddit.subreddit(str(subredditTrackEntry.get()))
                    username = str(usertoTrackEntry.get())

                    timeFilter = timeframeEntry.get()
                    results = list(subreddit.search('author:{}'.format(username), time_filter=timeFilter))
                    counter = 1
                    if results:
                        text_area.insert(INSERT, "User Name:  " + username + "\n\n")
                        for submission in results:
                            text_area.insert(INSERT, counter)
                            text_area.insert(INSERT, "\nTitle:  \n" + submission.title + "\n")
                            if (len(submission.selftext) != 0):
                                text_area.insert(INSERT, "\n" + "Text: \n" + submission.selftext + "\n")
                            dateAndTime = submission.created_utc
                            text_area.insert(INSERT,
                                             "\n" + "Date and Time: " + datetime.fromtimestamp(dateAndTime).replace(
                                                 tzinfo=timezone.utc).strftime("%m/%d/%Y %I:%M:%S %p %Z") + "\n")
                            text_area.insert(INSERT,
                                             "\n" + "Score: " + str(submission.score) + "\n *********************\n")
                            counter += 1
                            if (counter == 51):
                                break
                    else:
                        text_area.insert(INSERT,
                                         'User Name:  {} did not post in {} at the specified time frame!'.format(
                                             username, subreddit.display_name) + "\n")
                else:
                    timeframeLabel.configure(text="Enter hour, day, month or all!")
            else:
                text_area.insert(INSERT, "User or Subreddit does not exist.")

        else:
            if (len(usertoTrackEntry.get()) == 0):
                userExistLabel.configure(text="Please Enter Username.", fg="#AEB6BF")
            if (len(subredditTrackEntry.get()) == 0):
                subredditExistsLabel.configure(text="Please Enter Subreddit.", fg="#AEB6BF")
            if (len(timeframeEntry.get()) == 0):
                timeframeLabel.configure(text="Please enter timeframe", fg="#AEB6BF")

    timeframeLabel = Label(editor, text="Enter Timeframe:").grid(row=6, column=0, sticky=E, pady=15, padx=15)
    timeframeEntry = Entry(editor, width=35, borderwidth=5)
    timeframeEntry.grid(row=6, column=1, sticky=W)
    timeframeLabel = Label(editor, text="", fg="#AEB6BF")
    timeframeLabel.grid(row=7, column=0, sticky=E)

    emptyLabel1 = Label(editor, text="")
    emptyLabel1.grid(row=7, column=0)
    emptyLabel2 = Label(editor, text="")
    emptyLabel2.grid(row=8, column=0)
    searchButton = Button(editor, text="Search All", command=searchUserWithSubreddit)
    searchButton.grid(row=9, column=1)

    def prevPage():
        editor.destroy()
        import Configuration

    backButton = Button(editor, text="Previous Page", command=prevPage)
    backButton.grid(row=9, column=0)

    text_area_frame = Frame(editor)
    text_area_frame.grid(row=10, column=0, columnspan=3)

    text_area = scrolledtext.ScrolledText(text_area_frame, width=68, height=21, font=("Times New Roman", 13),
                                          bg="Alice blue")
    text_area.grid(row=0, column=0, pady=15, padx=15)

    # 3rd Button in main window


def createNewWindowTrackUserActivityOverTime():
    editor = Tk()
    editor.title('Track User Activity Over Time')
    editor.geometry("530x520")
    reddit = praw.Reddit('reddit-configuration-bot1')

    userToTrack = Label(editor, text="Username To Track:").grid(row=0, column=0, sticky=E, pady=15, padx=15)
    usertoTrackEntry = Entry(editor, width=35, borderwidth=5)
    usertoTrackEntry.grid(row=0, column=1, sticky=W)
    usertoTrackEntry.insert(0, "")
    userExistLabel = Label(editor, text="")
    userExistLabel.grid(row=1, column=0, sticky=E)

    def executeUserTracking():
        if (len(usertoTrackEntry.get()) != 0):
            userExists = searchUserExists(str(usertoTrackEntry.get()))
            if (userExists == False):
                userExistLabel.configure(text="User not found.    ", fg="#AEB6BF")
            else:
                userExistLabel.configure(text="User exists.     ", fg="#AEB6BF")
                userExists = True
        else:
            userExistLabel.configure(text="Please Enter Username.", fg="#AEB6BF")

    searchButtonUser = Button(editor, text="Search user", command=executeUserTracking)
    searchButtonUser.grid(row=2, column=1, sticky=W)
    timeframeLabel = Label(editor, text="Enter Timeframe:").grid(row=3, column=0, sticky=E, pady=15, padx=15)
    timeframeEntry = Entry(editor, width=35, borderwidth=5)
    timeframeEntry.grid(row=3, column=1, sticky=W)
    timeframeLabel = Label(editor, text="")
    timeframeLabel.grid(row=4, column=0, sticky=E)

    def searchComments():
        counter = 0
        if (
                timeframeEntry.get() == "hour" or timeframeEntry.get() == "day" or timeframeEntry.get() == "week" or timeframeEntry.get() == "month" or timeframeEntry.get() == "all"):
            timeframeLabel.configure(text="")
            text_area.insert(INSERT, "User Name:  " + usertoTrackEntry.get() + "\n\n")
            for submission in reddit.redditor(usertoTrackEntry.get()).comments.top(
                    time_filter=str(timeframeEntry.get())):
                counter = counter + 1
                # print(counter, ":  ", submission.body)
                text_area.insert(INSERT, str(counter) + ":  ")
                text_area.insert(INSERT, submission.body + "\n")
                dateAndTime = submission.created_utc
                text_area.insert(INSERT, "\n" + "Date and Time: " + datetime.fromtimestamp(dateAndTime).replace(
                    tzinfo=timezone.utc).strftime("%m/%d/%Y %I:%M:%S %p %Z") + "\n\n\n")
                if (counter == 10):
                    break
        else:
            timeframeLabel.configure(text="please enter hour, day, month or all!")

    searchButton = Button(editor, text="Search Comments", command=searchComments)
    searchButton.grid(row=4, column=1, sticky=W)
    text_area_frame = Frame(editor)
    text_area_frame.grid(row=5, column=0, columnspan=2)

    text_area = scrolledtext.ScrolledText(text_area_frame, width=60, height=19)
    text_area.grid(row=0, column=0, pady=15, padx=15)


################ INITIAL WINDOW USER INTERFACE ##############################

root = Tk()
root.title('User Behaviour Tracking on Reddit')
root.geometry("600x400")

clientIdLabel = Label(root, text="Enter Client ID:").grid(row=1, column=0)
clientIdEntry = Entry(root, width=30, borderwidth=5)
clientIdEntry.grid(row=1, column=1)
clientIdEntry.insert(0, initialize.clientID)
clientIdEntry.config(show="*")

clientSecretLabel = Label(root, text="Enter Client Secret:").grid(row=2, column=0)
clientSecretEntry = Entry(root, width=30, borderwidth=5)
clientSecretEntry.grid(row=2, column=1)
clientSecretEntry.insert(0, initialize.clientSecret)
clientSecretEntry.config(show="*")

usernameLabel = Label(root, text="Enter Username:").grid(row=3, column=0)
usernameEntry = Entry(root, width=30, borderwidth=5)
usernameEntry.grid(row=3, column=1)
usernameEntry.insert(0, initialize.username)

passwordLabel = Label(root, text="Enter Password:").grid(row=4, column=0)
passwordEntry = Entry(root, width=30, borderwidth=5)
passwordEntry.grid(row=4, column=1)
passwordEntry.insert(0, initialize.password)
passwordEntry.config(show="*")

userAgentLabel = Label(root, text="Enter User Agent:").grid(row=5, column=0)
userAgentEntry = Entry(root, width=30, borderwidth=5)
userAgentEntry.grid(row=5, column=1)
userAgentEntry.insert(0, initialize.userAgent)
userAgentEntry.config(show="*")
credLabel = Label(root, text="").grid(row=7, column=1)

def checkCredentials():
    if (len(clientIdEntry.get()) != 0 and len(clientSecretEntry.get()) != 0 and len(usernameEntry.get()) != 0 and len(
            passwordEntry.get()) != 0 and len(userAgentEntry.get()) != 0):
        try:
            reddit = praw.Reddit(client_id=str(clientIdEntry.get()),
                                 client_secret=str(clientSecretEntry.get()),
                                 username=str(usernameEntry.get()),
                                 password=str(passwordEntry.get()),
                                 user_agent=str(userAgentEntry.get()))
            reddit.redditor(str(usernameEntry.get())).id
            reddit.user.me
            emptyLable.configure(text="")
            showButtons()
            return True
        except prawcore.OAuthException:
            emptyLable.configure(text="Please enter correct credentials!!", fg="#AEB6BF")
            return False
        except ResponseException:
            emptyLable.configure(text="Please enter correct credentials!!", fg="#AEB6BF")
            return False
    else:
        emptyLable.configure(text="Please enter the fields!!", fg="#AEB6BF")

def showButtons():
    buttonKeywordUsage.grid(row=13, column=0)
    buttonUserActivity.grid(row=13, column=1)
    buttonSubmissionActivity.grid(row=13, column=2)
    labelKeywordUsage.grid(row=12, column=0, padx=20)
    labelUserActivity.grid(row=12, column=1, padx=20)
    labelTrackSubmissionActivity.grid(row=12, column=2, padx=20)


buttonSubmit = Button(root, text="Submit", command=checkCredentials, bg="cyan")
buttonSubmit.grid(row=9, column=1)
emptyLable = Label(root, text="")
emptyLable.grid(row=10, column=0)
emptyLable1 = Label(root, text="")
emptyLable1.grid(row=11, column=0)

labelKeywordUsage = Label(root, text="Track User Keyword Usage")
labelUserActivity = Label(root, text="Track User Activity in Subreddit")
labelTrackSubmissionActivity = Label(root, text="Track User Activity Over Time")

buttonKeywordUsage = Button(root, text="Search!", command=createNewWindowKeyWordUsage, bg="brown")
buttonUserActivity = Button(root, text="Search!", command=createNewWindowActivityTracking, bg="brown")
buttonSubmissionActivity = Button(root, text="Search!", command=createNewWindowTrackUserActivityOverTime, bg="brown")

root.mainloop()
