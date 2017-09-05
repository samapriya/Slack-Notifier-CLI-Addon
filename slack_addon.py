from slacker import Slacker
import os,csv,argparse,argparse
from os.path import expanduser
import getpass,subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#Slack Main Key
def slack_key_main():
    slackhome=expanduser("~/.config/slackkey/")
    if not os.path.exists(slackhome):
        os.mkdir(slackhome)
    print("Enter your SlackBot Admin Token")
    password=getpass.getpass()
    os.chdir(slackhome)
    with open("slack_main.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def slack_main_from_parser(args):
    slack_key_main()
    
#Slack Bot Key
def slack_key_bot():
    slackhome=expanduser("~/.config/slackkey/")
    if not os.path.exists(slackhome):
        os.mkdir(slackhome)
    print("Enter your SlackBot Bot Token")
    password=getpass.getpass()
    os.chdir(slackhome)
    with open("slack_key.csv",'w') as completed:
        writer=csv.writer(completed,delimiter=',',lineterminator='\n')
        writer.writerow([password])
def slack_bot_from_parser(args):
    slack_key_bot()
    
#Slack Message Post        
def botupdate(args):
    tkn=expanduser("~/.config/slackkey/slack_key.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your SlackBot Token")
        tk=getpass.getpass()
    if args.channel==None:
        args.channel='#general'
        slack=Slacker(tk)
        slack.chat.post_message(args.channel, args.msg)
    else:
        slack=Slacker(tk)
        slack.chat.post_message(args.channel, args.msg)

#Slack Message Update
def botfile(args):
    tkn=expanduser("~/.config/slackkey/slack_key.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your SlackBot Token")
        tk=getpass.getpass()
    if args.channel==None:
        args.channel='#general'
        slack=Slacker(tk)
        slack.files.upload(args.filepath,channels=args.channel,filename=args.fname,initial_comment=args.cmmt)
    else:
        slack=Slacker(tk)
        slack.files.upload(args.filepath,channels=args.channel,filename=args.fname,initial_comment=args.cmmt)

#Slack Delete all messages and files
def slackdelete():
    tkn=expanduser("~/.config/slackkey/slack_main.csv")
    if os.path.isfile(tkn):
        f=open(tkn)
        for row in csv.reader(f):
            tkin=str(row).strip("[']")
            tk=tkin
    else:
        print("Enter your Slack-Main Token")
        tk=getpass.getpass()
    subprocess.call('slack-cleaner --token '+tk+" --message --channel general --bot --perform --rate 1")
    subprocess.call('slack-cleaner --token '+tk+" --file --channel general --bot --perform --rate 1")
def slackdelete_from_parser(args):
    slackdelete()

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Slack API Addon')

    subparsers = parser.add_subparsers()
    parser_pp1 = subparsers.add_parser(' ', help='-------------------------------------------')
    parser_P = subparsers.add_parser(' ', help='-----Choose from Slack Tools Below-----')
    parser_pp2 = subparsers.add_parser(' ', help='-------------------------------------------')

    parser_slack_key_main = subparsers.add_parser('smain', help='Allows you to save your Slack Main API Token')
    parser_slack_key_main.set_defaults(func=slack_main_from_parser)

    parser_slack_key_bot = subparsers.add_parser('sbot', help='Allows you to save your Slack Bot API Token')
    parser_slack_key_bot.set_defaults(func=slack_bot_from_parser)
    
    parser_botupdate = subparsers.add_parser('botupdate', help='Allows your bot to post messages on slack channel')
    parser_botupdate.add_argument('--channel', help='Slack Bot update channel',default=None)
    parser_botupdate.add_argument('--msg', help='Slack Bot update message',default=None)
    parser_botupdate.set_defaults(func=botupdate)

    parser_botfile = subparsers.add_parser('botfile', help='Allows you to post a file along with comments')
    parser_botfile.add_argument('--channel', help='Slack Bot channel',default=None)
    parser_botfile.add_argument('--filepath', help='Slack Bot file path to upload',default=None)
    parser_botfile.add_argument('--cmmt', help='Slack Bot file comment',default=None)
    parser_botfile.add_argument('--fname', help='Slack Bot filename',default=None)
    parser_botfile.set_defaults(func=botfile)

    parser_slackdelete = subparsers.add_parser('slackdelete', help='Allows users to delete all messages and files posted by bots')
    parser_slackdelete.set_defaults(func=slackdelete_from_parser)

    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
