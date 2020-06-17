import argparse
from PlaylistDuration import PlaylistDuration

ap = argparse.ArgumentParser()
ap.add_argument('-u', '--url', required=False, help="URL Path")
args = vars(ap.parse_args())
my_url = args['url']

PlaylistDuration(my_url)