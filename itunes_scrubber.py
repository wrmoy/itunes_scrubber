import io
import os
import os.path
import platform
import plistlib
import sys
import urllib
import urlparse
import xml.etree.ElementTree

# Find iTunes Library XML
xml_path = os.environ['HOME']
if sys.platform == 'win32':
	if platform.release() == 'XP':
		xml_path = os.path.join(xml_path, 'My Documents', 'My Music', 'iTunes', 'iTunes Music Library.xml')
	elif platform.release() == 'Vista':
		xml_path = os.path.join(xml_path, 'Music', 'iTunes', 'iTunes Music Library.xml')
	elif platform.release() == '7' or platform.release() == '8':
		xml_path = os.path.join(xml_path, 'My Music', 'iTunes', 'iTunes Music Library.xml')
	else:
		print "Platform not supported"
		sys.exit(1)
elif sys.platform == 'darwin':
	xml_path = os.path.join(xml_path, 'Music', 'iTunes', 'iTunes Music Library.xml')
else:
	print "System not supported"
	sys.exit(1)

# Check each track to see if its associated file exists
print "Loading iTunes library..."
try:
	itunes_plist = plistlib.readPlist(xml_path)
except:
	print "Could not open iTunes XML"
	sys.exit(1)
to_remove = []
total_tracks = len(itunes_plist['Tracks'])
count = 1
print ''
for track_id, track in itunes_plist['Tracks'].iteritems():
	track_path = urllib.url2pathname(urlparse.urlparse(track['Location']).path)
	if not os.path.isfile(track_path):
		to_remove.append(track_id)
	sys.stdout.write("\r Scanning... " + str(count) + "/" + str(total_tracks))
	count += 1
print ''

# Remove tracks with no associated file from dictionary
for track_id in to_remove:
	print "Removing " + itunes_plist['Tracks'][track_id]['Name']
	del itunes_plist['Tracks'][track_id]

# Write dictionary back to file
with open(xml_path + ".new", 'w') as f:
	f.write(plistlib.writePlistToString(itunes_plist))

print "Finished scrubbing"