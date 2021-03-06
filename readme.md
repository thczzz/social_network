## social_network - REST api
##### Simple social network - using Django, DRF and PostgreSQL, Session Authentication


Build an image if necessary, then Run the server and db in Docker containers + Auto Creates an admin user via create_superuser.sh (username: admin, password: admin)
```
docker-compose build
docker-compose up
  --OR--
docker-compose -f <path/to/docker-compose.yml> build
docker-compose -f <path/to/docker-compose.yml> up
```


Docker info:
```
python image version: 3.6
postgreSQL:
  - ip: 192.168.99.100 (default, as specified in core/settings.py)
  - port: 5432
```

#

Authentication endpoints:
```
api-auth/login/
api-auth/register/
api-auth/logout/
```
#
User endpoints:
```
api/user/friends/<int:user_id>/
```
**Get user's friends, by providing "user_id": int. (login required, GET only) 

```
api/user/send-friend-request/<int:to_user>/
```
**Sends a friend request to another user, by providing a "to_user": int. (login required, POST only)
```
api/user/friend-requests/
```
**Returns all of your pending friend requests. (login required, GET only)
```
api/user/friend-requests/<int:friend_req_id>/
```
**Accept a friend request by providing "friend_req_id": int.(login required, POST only)
#
Post endpoints:
```
api/posts/add/
```
**Add a post(login required, POST req only)

```
api/posts/wall/
```
**Returns posts by user's friends, Recent Posts first(made in the last 10 minutes) ordered by num_of_comments desc, num_of_likes desc, the rest are ordered by created_at desc, num_of_likes desc (login required, GET only)

```
api/posts/view/<int:user_id>/
```
**Returns all the posts for a user by providing "user_id": int.(login required, GET only)

```
api/posts/like/<int:post_id>/
```
**Like/Unlike a post(login required, POST only)
```
api/posts/comment/<int:post_id>/
```
**Add a comment to a post. (login required, POST only)
