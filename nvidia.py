from adb import adb_commands
from adb.sign_pythonrsa import PythonRSASigner

class shield():
	# Change this to your Nvidia Shield IP address
	shield_ip_and_port = b'192.168.1.100:5555'
	
	buttons = { 
		'power': 'KEYCODE_POWER',
		'sleep': 'KEYCODE_SLEEP',
		'wake': 'KEYCODE_WAKEUP',
		'home': 'KEYCODE_HOME',
		'back': 'KEYCODE_BACK',
		'search': 'KEYCODE_SEARCH',
		'up': 'KEYCODE_DPAD_UP',
		'down': 'KEYCODE_DPAD_DOWN',
		'left': 'KEYCODE_DPAD_LEFT',
		'right': 'KEYCODE_DPAD_RIGHT',
		'center': 'KEYCODE_DPAD_CENTER',
		'volume up': 'KEYCODE_VOLUME_UP',
		'volume down': 'KEYCODE_VOLUME_DOWN',
		'rewind': 'KEYCODE_MEDIA_REWIND',
		'ff': 'KEYCODE_MEDIA_FAST_FORWARD',
		'play/pause': 'KEYCODE_MEDIA_PLAY_PAUSE',
		'previous': 'KEYCODE_MEDIA_PREVIOUS',
		'next': 'KEYCODE_MEDIA_NEXT',
	}

	apps = {
		'hbo': 'com.hbo.hbonow/com.hbo.go.LaunchActivity',
		'prime': 'com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity',
		'music': 'com.google.android.music/.tv.HomeActivity',
		'youtube': 'com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity',
		'ted': 'com.ted.android.tv/.view.MainActivity',
		'games':'com.nvidia.tegrazone3/com.nvidia.tegrazone.leanback.LBMainActivity'
	}

	def __init__( self ):
		self.connect()

	def connect( self ):
		signed_key = PythonRSASigner.FromRSAKeyPath( 'adbkey' )
		self.device = adb_commands.AdbCommands().ConnectDevice( serial=self.shield_ip_and_port, rsa_keys=[ signed_key ] )

	def shell( self, arg ):
		for i in range( 3 ):
			try:
				self.device.Shell( arg )
				return
			except ConnectionResetError:
				self.connect()

	def press( self, button ):
		if button not in self.buttons:
			return { 'error': f'unknown button "{button}"'}

		self.device.Shell( f'input keyevent {self.buttons[ button ]}' )

	def launch( self, app ):
		if app not in self.apps:
			return { 'error': f'no such app "{app}"' }

		app_launch_activity = self.apps[ app ]
		self.device.Shell( f'am start -n {app_launch_activity}')