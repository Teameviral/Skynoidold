import os

from pydrive import auth
from pydrive.drive import GoogleDrive
from pyrogram import filters

from skynoid import setbot, AdminSettings, gauth, GDRIVE_CREDENTIALS, ENV
from skynoid.languages.strings import tld
from skynoid.utils import filt


@setbot.on_message(filters.user(AdminSettings) & filt.command(['gdrive']))
async def gdrive_helper(_, message):
    if len(message.text.split()) == 1:
        gdriveclient = os.path.isfile('client_secrets.json')
        if ENV:
            if not GDRIVE_CREDENTIALS:
                await message.reply(tld('gdrive_credential_err_heroku'))
                return
            elif not gdriveclient:
                with open('client_secrets.json', 'w') as gfile:
                    gfile.write(GDRIVE_CREDENTIALS)
                    gfile.close()
                gdriveclient = os.path.isfile('client_secrets.json')
        if not gdriveclient:
            await message.reply(tld('gdrive_credential_err'))
            return

        gauth.LoadCredentialsFile('skynoid/session/drive')
        if gauth.credentials is None:
            try:
                authurl = gauth.GetAuthUrl()
            except auth.AuthenticationError:
                await message.reply(
                    'Wrong Credentials!'
                    'Check var ENV gdrive_credentials on heroku'
                    'or do .credentials (your '
                    'credentials) for change your Credentials',
                )
                return
            teks = (
                'First, you must log in to your Google drive first.\n\n'
                '[Visit this link and login to your Google '
                'account]({})\n\nAfter that you will get a verification code,'
                'type `/gdrive (verification code)` '
                "without '(' or ')'.".format(authurl)
            )
            await message.reply(teks)
            return
        await message.reply(
            "You're already logged in!\nTo logout type `/gdrive logout`",
        )
    elif len(
        message.text.split(),
    ) == 2 and message.text.split()[1] == 'logout':
        os.remove('skynoid/session/drive')
        await message.reply(
            'You have logged out of your account!',
        )
    elif len(message.text.split()) == 2:
        try:
            gauth.Auth(message.text.split()[1])
        except auth.AuthenticationError:
            await message.reply('Your Authentication code is Wrong!')
            return
        gauth.SaveCredentialsFile('skynoid/session/drive')
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile(
            {'q': "'root' in parents and trashed=false"},
        ).GetList()
        for drivefolders in file_list:
            if drivefolders['title'] == 'Skynoid Drive':
                await message.reply(
                    'Authentication successful!\nWelcome back!',
                )
                return
        mkdir = drive.CreateFile(
            {
                'title': 'Skynoid Drive',
                'mimeType': 'application/vnd.google-apps.folder',
            },
        )
        mkdir.Upload()
        await message.reply(
            'Authentication successful!',
        )
    else:
        await message.reply('Invaild args!\nCheck /gdrive for usage guide')
