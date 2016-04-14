# Corgi: Capture Org Instantly

## What Corgi does

Corgi allows you to:

* Quickly capture tasks and insert them into an Emacs `org-mode` file from anywhere on your computer

* Capture tasks from mobile devices to an `org-mode` file

* Sync tasks in an `org-mode` file with a `taskpaper` file for use on mobile devices

Corgi also includes several helpful functions for parsing various aspects of a `.org` file. For example, there are functions to convert between Python `datetime` objects and `org-mode` timestamps:

```python
>>> from corgi.parse import org_timestamp_to_dt, dt_to_org_timestamp
>>> dt = org_timestamp_to_dt('<2016-04-27 Wed 11:30>')
>>> dt
datetime.datetime(2016, 4, 27, 11, 30)
>>> dt_to_org_timestamp(dt)
'<2016-04-27 Wed 11:30>'
```

## Setting up Corgi

The first thing you will need to do is fill in some values in the `.corgi` configuration file. At the minimum, you should enter a values for:

* `corgi_home` under `[paths]`: the location where where your `taskpaper` files and sync file (the file your tasks will initially go to when you capture from a mobile device or from the Corgi UI.
* `org_file` under `[paths]`: the location of the `.org` file where you keep your tasks

After running Corgi's `setup.py` file, you will need to bind the `runcorgi.sh` script to a global key combination so that the app can be triggered from anywhere on your computer. On Ubuntu this can be done as follows:

1. Go to **System Settings**, click on the **Keyboard** icon, and then select the **Shortcuts** tab.
2. Select **Custom Shortcuts** and then hit the **+** symbol to add a new keyboard shortcut.
3. For the name, enter **Corgi** or whatever you want, and for the command, enter the full path the `runcorgi.sh` script.
