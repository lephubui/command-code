# xflowbot/app.py
# Flask application for XFlowBot to post messages on X (formerly Twitter)
from flask import Flask, request, redirect, session, url_for, render_template
import tweepy
from urllib.parse import urlparse, parse_qs
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow HTTP for local dev only

app = Flask(__name__)
app.secret_key = 'whatisxflowbot'  # Change to a random string for session security

# Hardcoded credentials for testing - REPLACE WITH YOURS, REMOVE FOR PRODUCTION
CONSUMER_KEY = os.getenv('CONSUMER_KEY')  # Your Consumer Key (API Key)
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')  # Your Consumer Secret (API Secret Key)
REDIRECT_URI = os.getenv('REDIRECT_URI')  # Your Redirect URI

@app.route('/')
def home():
    logged_in = 'oauth_token' in session and 'oauth_token_secret' in session
    return render_template('dashboard.html', logged_in=logged_in)

@app.route('/login')
def login():
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY, CONSUMER_SECRET,
        callback=REDIRECT_URI
    )
    try:
        auth_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(auth_url)
    except tweepy.errors.TweepyException as e:
        return f"Login error: {str(e)}"

@app.route('/callback')
def callback():
    request_token = session.get('request_token')
    if not request_token:
        return "No request token in session - re-try login", 400
    
    verifier = request.args.get('oauth_verifier')
    if not verifier:
        return "No verifier in callback - authorization denied", 400
    
    auth = tweepy.OAuth1UserHandler(
        CONSUMER_KEY, CONSUMER_SECRET,
        callback=REDIRECT_URI
    )
    auth.request_token = session['request_token']  # Use the full dict
    try:
        access_token, access_token_secret = auth.get_access_token(verifier)
        session['oauth_token'] = access_token
        session['oauth_token_secret'] = access_token_secret
        return redirect(url_for('home'))
    except tweepy.errors.TweepyException as e:
        return f"Callback error: {str(e)}"

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    session.pop('oauth_token_secret', None)
    session.pop('request_token', None)
    return redirect(url_for('home'))

@app.route('/post_message', methods=['POST'])
def post_message():
    if 'oauth_token' not in session or 'oauth_token_secret' not in session:
        return "Login required", 401
    
    try:
        message = request.form.get('message', '').strip()
        if not message:
            return "No message provided", 400
        
        print("Posting with oauth_token:", session['oauth_token'])  # Debug
        print("oauth_token_secret:", session['oauth_token_secret'])  # Debug (remove in production)
        
        auth = tweepy.OAuth1UserHandler(
            CONSUMER_KEY, CONSUMER_SECRET,
            session['oauth_token'], session['oauth_token_secret']
        )
        api = tweepy.API(auth)
        print("API initialized successfully")  # Debug
        status = api.update_status(status=message)
        print("status:", status)  # Debug
        post_id = status.id
        
        return f"Message posted successfully with ID: {post_id}"
    except tweepy.errors.TweepyException as e:
        return f"Error posting message: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)