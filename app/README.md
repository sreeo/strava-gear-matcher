### Short description
I have a bunch of shoes I cycle through different days of the week.

This is how it works:
1. Add your gear on your strava profile (shoe or cycle).
2. Do your workout (run/cycle).
3. Login via strava on the app, and update the description for all your gear. 
4. Keep descriptions detailed, describing color, make and any branding, it helps while matching.
5. Click on Update Gear for Activity, take a photo of the gear you used. 
6. The app will try to match the photo of the gear uploaded to the existing gear associated with the account. The description/name is taken into considering while trying to match.






### Internal
1. I used the OPENAI Clip model to get the image features and the description features.
2. And then do a cosine similarity for all gear and image vectors, and return the highest ranked similarity score/gear.




