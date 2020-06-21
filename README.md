# pass-boi
A minimalist passwords manager for your local device.

## How to use?
### 1) Open a terminal or cmd.
### 2) Open the pass-boi/src directory.
### 3) Run main.py
`python main.py`

## Usage
```
login user      =   login Username
logout user     =   logout
create user     =   new user Username
delete user     =   delete user Username
add password    =   new password "key" "password"
get password    =   get password "key"
update password =   update password "key" "old-password" "new-password"
delete password =   delete password "key" "password"
get keys        =   get keys
get users       =   get users
```
## Example

```
pass-boi REPL started !
type 'exit' to exit...  
==--------------------==
[NotLoggedIn] >> new user imuas
[NotLoggedIn] >> login imuas
[imuas] >> new password "some-website.com" "password123"
[imuas] >> get keys
"some-website.com"
[imuas] >> get password "some-website.com"
"some-website.com" : "password123"
[imuas] >> update password "some-website.com" "password123" "123password"
[imuas] >> get password "some-website.com"
"some-website.com" : "123password"
[imuas] >> logout
[NotLoggedIn] >> get users
[1]: imuas
[NotLoggedIn] >> exit
```
