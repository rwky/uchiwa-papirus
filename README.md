This is a simple script which uses a [Pi Supply PaPiRus](https://github.com/PiSupply/PaPiRus) to
update the screen with the status from [uchiwa](https://www.uchiwa.io).

It just requires python3 and the PaPiRus library installed.

Configuration can be done through environment variables an example would be

```
export AUTH_USER=user
export AUTH_PASSWD=password
export AUTH_REALM=realm
export URL='https://domain.com/events?token=api-token'
```

I put sensu behind nginx with basic auth hence the `AUTH_*` variables.

I use a Pi2 with a large hat, it looks like this:

![OK image](https://raw.githubusercontent.com/rwky/uchiwa-papirus/master/ok.jpg)
![Problem image](https://raw.githubusercontent.com/rwky/uchiwa-papirus/master/problem.jpg)
