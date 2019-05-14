# Comics publisher

Program for publishing [xkcd comics](https://xkcd.com/) to VK Community.


### How to install

For proper use you have to get VK account. You need to create [standalone  VK app](https://vk.com/dev) and get `client_id`.

Than you need `access_token` which you can get by `Implicit Flow` method described [here](https://vk.com/dev/implicit_flow_user).
Use `photos`, `groups`, `wall` and `offline` for `scope` parameter.
Y
ou also need to get `group_id` of VK Community where you wish to post comics (please refer to [this service](http://regvk.com/id/))

After that copy the file `.env-example` to `.env` and paste your `client_id`, `access_token` and `group_id`.

Python3 should be already installed. 
It is strictly recommended that you use [virtual environment](https://docs.python.org/3/library/venv.html) for project isolation. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).