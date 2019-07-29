This is used to find posts in Community that you have not replied to that have the label "Achievement"

Open Chrome browser and type chrome://version/ in the search bar.
The first line of the returned page should say something like: Google Chrome 75.0.3770.100 (Official Build) (64-bit)

Open requirements.txt and edit the line "chromedriver-binary==75.0.3770.140" so the release number matches your chrome version.

If you are using Chrome version 76, use chromedriver-binary==76.0.3809.68
If you are using Chrome version 75, use chromedriver-binary==75.0.3770.140
If you are using Chrome version 74, use chromedriver-binary==74.0.3729.6
If you are using Chrome version 73, use chromedriver-binary==73.0.3683.68

If you are on a Mac, you can use homebrew to install chromdriver with this command:
brew cask install chromedriver

*Install requirements:*
cd to linux_academy folder
pip install -r requirements.txt

*Enter login credentials*
Make a copy of pw_blank.py and rename it to pw.py. At the top of the file, replace USERNAME with your username, and PASSWORD with your password.

You will need to enable less secure applications if you are sending this via your LinuxAcademy Gmail account.
https://myaccount.google.com/lesssecureapps

*Run the script:*
python notify.py
