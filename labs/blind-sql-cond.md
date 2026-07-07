# Blind SQL injection with conditional responses

[Portswigger Lab URL](https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses)

## Description

```
This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.
The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.
To solve the lab, log in as the administrator user. 
```

## Notes

Inspecting the request to the lab's server in OWASP ZAP, I see the following header:
`Cookie: TrackingId=ABKYiriquzzxlI8X; session=nKRP9LlYQVrPYtQk95P3lvyLtvqQhRnG`

Modifying the `TrackingId` part should be the SQL injection here - let's check.
Indeed, when passing `' AND 1=1--`, the welcome message stays there,
while with `' AND 1=2--`, it disappears. This single bit of extracted
information is enough to extract the admin's password.

There are 2 parts, getting the password length and then recovering it character
by character.

The length query would look something like:

```
AND LENGTH(SELECT password FROM users WHERE username='administrator') > 3
```

No need for a script here, since there aren't that many possibilities here.
So, URLEncode and test with ZAP.
Hmm, putting `' OR LENGTH(SELECT password FROM users WHERE username='administrator') > 3--`
seems to make the message disappear, so I think there's something wrong with the query here.
`' AND LENGTH('abcd') > 3--` seems to work.

Apparently, I was doing the query wrong - the inner select needs to be
wrapped in one more set of parentheses. So this works:

```
' AND LENGTH((SELECT password FROM users WHERE username='administrator')) > 0--
```

The length is 20. `>19` shows the message, but at `>20`, it disappears.
Now, for actually bruteforcing 20 characters one-at-a-time, I do need a
script.


Actually, I ended up implementing the password length search in the script
as well. Since the requests don't go through very fast, I implemented
binary search both for the password length and for the ASCII value of
each of the password letters.

The full script is in [blind-sql-cond.py](blind-sql-cond.py), and it
successfully solves the lab.


