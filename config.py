# main
data_file						=	'data.txt'

# window titles
ScreenName						=	'KeyHolder'
LockScreen_ScreenName			=	'KeyHolder'
MainScreen_ScreenName			=	'KeyHolder'

# window size
width							=	500
height							=	450
left							=	400
top								=	150

#colors
MainBackgroundColor				=	'#FFFFFF'
LockScreen_BackGroundColor		=	'#FFFFFF'

# buttons' names
unlock_button					=	'Unlock'
lock_button						=	'Lock'
lock_button_up					=	'Back'
add_button						=	'Add'
help_button						=	'Help'
exit_button						=	'Exit'

# descriptions
description						=	'That KeyLocker that keeps all data incryptedly'
auther							=	'Author: Riniyar Kerendey (riniyar8@gmail.com)'
version							=	'Version: 1.0'

# help
help_msg="""Program let u to add and update data, that'll be incryted by AES
(Main task was to keep passwords for accounts on different sites)

Password: First time u write any password u want
Afterwards it'll be password of ur starage
U cannot change it! (only delete data file)

All data has tree-like data structure:
1 level: set of sites;
2 level: set of accounts on this site;
last level: set of key-value notes (<key> : <value>)"""