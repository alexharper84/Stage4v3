import os
import webapp2
import jinja2


from content import SECTIONS, guestbook_key, Submission, DEFAULT_GUESTBOOK_NAME

template_dir = os.path.join(os.path.dirname(__file__), 'html_templates')
jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, sections=SECTIONS, **kw))

class MainPage(Handler):
	def get(self):
		self.render("/main_page.html", page_name="home")

class SubmissionListHandler(Handler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		submissions_query = Submission.query(
		ancestor=guestbook_key(guestbook_name)).order(-Submission.date)
		num_submissions = 1000
		submissions = submissions_query.fetch(num_submissions)
		self.render('guestbook.html', submissions=submissions, page_name="submissions")

class SubmissionHandler(Handler):
	def get(self, **kwargs):
		self.render('add_submission.html', page_name="submissions", **kwargs)

	def post(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		submission = Submission(parent=guestbook_key(guestbook_name))
		submission.name = self.request.get('name')
		submission.link = self.request.get('link')
		submission.user_comment = self.request.get('user_comment')

		query_params = {"guestbook_name" : guestbook_name,
						"name": submission.name,
						"link":submission.link,
						"user_comment":submission.link,
						}

		is_valid, errors = validate_submission(submission, self.request.get(''))

		if is_valid:
			submission.put()
			self.redirect('/comments_section/')
		else:
			for k, v in errors.items():
				query_params[k] = v
			self.get(**query_params)


def validate_submission(submission, null):
	valid = True
	errors = {}
	min_name_length = 2
	min_comment_length = 10

	if len(submission.name) < min_name_length:
		errors['name_error'] = "A VALID NAME IS LONGER THAN TWO LETTERS."
		valid = False
	if len(submission.user_comment) < min_comment_length:
		errors['user_comment_error'] = "A VALID COMMENT IS LONGER THAN TEN LETTERS."
		valid = False

	return valid, errors
