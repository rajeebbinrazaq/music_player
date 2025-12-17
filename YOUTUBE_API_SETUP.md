# YouTube API Setup Guide

Follow these steps to get your free YouTube Data API v3 key:

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top
4. Click "New Project"
5. Enter a project name (e.g., "Music Player App")
6. Click "Create"

## Step 2: Enable YouTube Data API v3

**Note: For simple testing, you can skip this!** The app now supports adding individual videos via URL using oEmbed without an API key. However, for Search functionality, the API key is still required.

1. In the Google Cloud Console, make sure your new project is selected
2. Go to "APIs & Services" > "Library" (or click [here](https://console.cloud.google.com/apis/library))
3. Search for "YouTube Data API v3"
4. Click on "YouTube Data API v3"
5. Click the "Enable" button

## Step 3: Create API Credentials

1. Go to "APIs & Services" > "Credentials" (or click [here](https://console.cloud.google.com/apis/credentials))
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "API key"
4. Your API key will be created and displayed
5. **Copy the API key** - you'll need this for the next step

## Step 4: (Optional) Restrict Your API Key

For security, it's recommended to restrict your API key:

1. Click on the API key you just created
2. Under "API restrictions":
   - Select "Restrict key"
   - Check "YouTube Data API v3"
3. Under "Application restrictions" (optional):
   - You can restrict by HTTP referrers, IP addresses, etc.
4. Click "Save"

## Step 5: Configure ERPNext

Now add the API key to your ERPNext site:

```bash
cd /opt/bench/bench-expiriments
bench --site experiments.bench set-config youtube_api_key "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with the API key you copied in Step 3.

## Step 6: Verify Configuration

To verify the API key is configured correctly:

```bash
bench --site experiments.bench console
```

Then in the console:
```python
import frappe
api_key = frappe.conf.get('youtube_api_key')
print(f"API Key configured: {api_key[:10]}..." if api_key else "No API key found")
exit()
```

## API Quota Information

The YouTube Data API v3 has a free quota of **10,000 units per day**.

### Cost per operation:
- **Search**: 100 units per request
- **Video details**: 1 unit per request

### What this means:
- You can perform approximately **100 searches per day**
- Or fetch details for **10,000 videos per day**
- Or a combination of both

### Tips to manage quota:
1. Cache search results when possible
2. Avoid unnecessary API calls
3. Use video details sparingly
4. Consider implementing rate limiting for multiple users

### Monitoring quota usage:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Dashboard"
3. Click on "YouTube Data API v3"
4. View your quota usage and limits

## Troubleshooting

### "API key not valid" error
- Double-check that you copied the entire API key
- Ensure the YouTube Data API v3 is enabled for your project
- Check if your API key has the correct restrictions

### "Quota exceeded" error
- You've used up your daily quota of 10,000 units
- Wait until the next day (quota resets at midnight Pacific Time)
- Consider requesting a quota increase from Google

### "The request cannot be completed because you have exceeded your quota"
- This means you've hit the daily limit
- You can request a quota increase in the Google Cloud Console
- Or wait for the quota to reset

## Requesting Quota Increase

If you need more than 10,000 units per day:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Quotas"
3. Find "YouTube Data API v3"
4. Click "Edit Quotas"
5. Fill out the quota increase request form
6. Explain your use case
7. Submit the request

**Note**: Quota increases are reviewed by Google and may take several days to be approved.

## Alternative: YouTube API Alternatives

If you need more quota or want to avoid API limits, consider:

1. **YouTube Music API** (unofficial, no quota limits but against ToS)
2. **Spotify API** (different service, but has generous free tier)
3. **SoundCloud API** (for SoundCloud content)
4. **Local file playback** (no API needed)

## Security Best Practices

1. **Never commit your API key to version control**
2. **Use environment variables or site config** (as we're doing)
3. **Restrict your API key** to only the APIs you need
4. **Monitor usage** regularly in Google Cloud Console
5. **Rotate keys** periodically for security
6. **Use IP restrictions** if your server has a static IP

## Support Links

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)
- [YouTube API Support](https://support.google.com/youtube/topic/9257096)

---

**Important**: Make sure to comply with [YouTube's Terms of Service](https://www.youtube.com/t/terms) and [API Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service) when using this app.
