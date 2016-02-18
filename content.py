from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

SECTIONS = [
	{"title"     : "ADD A COMMENT",
	 "href"      : "comments_section/",
	 "short_title":"COMMENTS SECTION",
	 "id"        : "submissions",
	 "alt"			 : "tell me how you really think..."}]

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	return ndb.Key('Guestbook', guestbook_name)

class Submission(ndb.Model):
  """A main model for representing an individual Guestbook entry."""
  link = ndb.StringProperty(indexed=False, required=True)
  user_comment = ndb.StringProperty(indexed=False, required=True)
  date = ndb.DateTimeProperty(auto_now_add=True)
  name = ndb.StringProperty(indexed=False, required=True)
