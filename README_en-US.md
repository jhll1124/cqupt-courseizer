# cqupt-courseizer

### Freshmen, how can you compete with your senior in computer science for courses? 😋

> If you find it useful, please give it a ⭐Star ～(∠・ω< )⌒⭐

## Instructions

This script can free your hands and make you faster than others!  
It can search for courses containing specified keywords in cross-disciplinary general education courses (Humanities and Social Sciences, Natural Sciences and Technology) and automatically start concurrent course grabbing.  
Currently, it does not support curriculum courses ~~because you have to learn them even if you don't want to~~

## Build from Source

This project is built with Python 3.13 and theoretically supports most Python3 versions.

### Install Dependencies (skip if already installed)

```bash
    pip3 install requests
```

### Clone the Project

```bash
    git clone --depth=1 https://github.com/jhll1124/cqupt-courseizer.git
```

> You can also directly Download Zip

### Change the cookie and search_ls in the main function of main.py

Then you can start grabbing courses happily!  
By default, it grabs once every 0.5 seconds. You can change the interval by modifying the parameters of the `loop_rob` function in `grabber.py`.

> To prevent abuse, you need to obtain the cookie and course list yourself. The cookie in the source code is just an example.

## Obtain Cookie

Choose one of the following methods

1. Press F12 in the browser to open the developer tools, select a request in the network tab, and find it in the request headers.
2. Enter `javascript:alert(document.cookie)` in the browser's address bar (case insensitive)~~(some parts may be eaten by the browser)~~
3. Use the browser plugin [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

## Tips

1. This script is only applicable to pre-selection courses, not for re-selection courses.
2. The server resets the session every few hours (currently unknown), so you need to refill the cookie.
3. This version is still in testing. If there are any bugs, please submit an issue.

## Other Features

Explore the source code yourself~ ~~Definitely not because I'm too lazy to write~~

## Acknowledgements

> Thanks to the following projects for providing inspiration and ideas for this project

[cqupt-grabber](https://github.com/LgoLgo/cqupt-grabber)

## License

This project uses the GPLv3 license, allowing free use, modification, and distribution of the code, but must comply with the corresponding terms, including indicating the original author and modification content, providing the source code, and keeping the GPLv3 license, as well as granting contributors the right to use their patents. This project is provided "as is" without any form of warranty. For the full license, please see [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).
