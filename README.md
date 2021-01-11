# SpotifyApi
It is a class based api. It makes multiple get request with the spotify.

#### How to setup the Api :-
1. First install requirements.txt by :-
`python3 install -r requirements.txt`
2. Enter the `client id` and `secret key` that you have get from the spotify developer account in the "spotify_api.py".
3. Make a object of the class to use methods.
<br>Example:-
<br>`spotify = SpotifyApi()`
4. Then you have to perform authentication for getting the access token. A _access token_ is used to make get request. One need to understand that access token has a expiry time i.e **_3600 seconds_** for version 1 now. But your class automatically manages that work for you. It will regenerate the token if expires. So you don't need to worry about it at all. Running authentication is one time process. For authentication simply run :-
<br>`spotify.perform_auth()`
<!-- -->
#### How to use the Api:
1. Now you can start using the methods or get requests as shown below :-
<br>`spotify.search(query, operator=None, operator_query=None, search_type="type")`
<br>where :-
<br>**query** = It can be anything depending on the type of search. For search type like artist, it can be Neha Kakkar, Honey Singh, Raaftar etc.
<br>**_search_type_** = spotify provides different type of searches like by artists, albums or tracks.
<br>_**operator**_ = spotify provides two type of operator i.e "**OR**" and "**NOT**". NOT operator means exclude it. OR operator means anyone of both.
<br>**_operator_query_** = means anything you want to exclude or to make an option.
example :-
<br>`songs=spotify.search("Tony", operator="not" , operator_query="Kakkar", search_type="artist")`
<br> The above code will search for tony but it will neglect the results which contains the Kakkar in their title.
2. You can even search for the track in the similar way for track. Example :-
<br>`spotify.search(Time, search_type="track")`

**Note : -**
<br>You can use this Spotify Api Client without any issue. Feel free to suggest changes.

**Last Test : -**
<br>12 January 2021