from tango.factory.app import build_app

app = build_app('hybrid')
app.this_was_added_after_stash = 'Hello, world!'
