Frest
=====
<img src="https://raw.githubusercontent.com/h4wldev/frest/master/frest.png" height="150">

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/h4wldev/Frest/blob/master/LICENSE)

Frest is the frame of the restful api server created with [pallets/flask](https://github.com/pallets/flask).

## GOAL
Basic restful api server including login, sign up, sign out, modify account, writing, and etc..

## Getting Started
Just modify [`app/config`](https://github.com/h4wldev/Frest/blob/master/app/config.py) and use it.

## FEATURE
### 1.0.1
__API__
- `GET /api/v@/users/<prefix(me or user_id)>` Return user information
- `POST /api/v@/users/<prefix(me or user_id)>` Modify user information
- `DELETE /api/v@/users/<prefix(me or user_id)>` Delete user

__FEATURE__
- You can expire token with function `app/modules/token` token_expire_with_id, token_expire_with_token

__ETC__
- Edit some files code convention
- Delete Form validation. Instead, use wtform

### 1.0.0
__API__
- `GET /api/v@/auth` Login using 'HTTP basic auth' and generate token
- `GET /api/v@/token` Login using 'HTTP token auth'
- `GET /api/v@/users` Get users with token and params: page(Default: 0), limit(Default: 10)
- `POST /api/v@/users` Sign Up

__FUNCTION__
- ~~Form validation `app/modules/form_validation`~~ __Now Removed__
- Auto route loading `app/routes`
- Decorating return values `app/modules/frest/api`

## TODO
- Token <-> database connect

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
