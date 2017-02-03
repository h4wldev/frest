Frest
=====
<img src="https://raw.githubusercontent.com/h4wldev/frest/master/frest.png" height="150">

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/h4wldev/Frest/blob/master/LICENSE)

Frest is the frame of the restful api server created with [pallets/flask](https://github.com/pallets/flask).

## GOAL
Basic restful api server including login, sign up, sign out, modify account, writing, and etc..

## Getting Started
Just modify [`app/config`](https://github.com/h4wldev/Frest/blob/master/app/config.py) and `python app.py runserver` use it.

## FEATURE
__API__
- `GET /api/v@/` Return environment, versions
- `GET /api/v@/auth` Login using 'HTTP basic auth' and generate token
- `POST /api/v@/logout` Sign out
- `GET /api/v@/users` Get users with token and params: page(Default: 0), limit(Default: 10)
- `POST /api/v@/users` Sign Up
- `GET /api/v@/users/<prefix(me or user_id)>` Return user information
- `PUT /api/v@/users/<prefix(me or user_id)>` Modify user information
- `DELETE /api/v@/users/<prefix(me or user_id)>` Delete user
- `GET /api/v@/token?type=extension&token=<token>` Token expire time extension 
- `GET /api/v@/users/<prefix(me or user_id)>/login_histories` Return Login histories with token and params: page(Default: 0), limit(Default: 10)

__FUNCTION__
- Auto route loading `app/routes`
- Decorating return values `app/modules/frest/api`
- You can expire token with function `app/models/user_token_model` token_expire_all, token_expire_with_token

## TODO
- User role development 

## License
Copyright (c) 2017 Hawl Kim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
