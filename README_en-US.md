# cqupt-courseizer

### Freshmen, how can you compete with your senior in computer science for courses? 😋

> If you find this useful, please give it a ⭐Star ～(∠・ω< )⌒⭐

This English document is translated with the support of GitHub Copilot.

## Project Introduction

This Python script can free your hands and get you ahead of others!  
It can search for courses containing specified keywords in the cross-disciplinary general education courses (Humanities and Social Sciences, Natural Sciences and Technology) and automatically start concurrent course selection.  
Currently, it does not support required courses ~~because you have to take them anyway~~.
Now supports required courses because some professional elective courses in certain majors are ~~too hard to grab~~.

## Build from Source

This project is built with Python 3.13 and theoretically supports versions above 3.6.

### Install Dependencies (Skip if already installed)

> If you don't have a Python interpreter, download it from the [official website](https://www.python.org/downloads/).

```bash
pip3 install requests
```

### Clone the Project

```bash
git clone --depth=1 https://github.com/jhll1124/cqupt-courseizer.git
```

> You can also directly Download Zip

```bash
wget https://github.com/jhll1124/cqupt-courseizer/archive/refs/heads/main.zip
```

### Change the `cookie` and `search_ls` in the main function of `main.py`

Then you can start grabbing courses happily!  
For each string in search_ls, as long as the course information contains it, it will grab the course. It supports course id, name, instructor, etc.  
To ensure accuracy, fuzzy search is not supported.  
There are three pre-programmed robbing speeds, and the interval can be changed by modifying the `mode` parameter of the `loop_rob` function.  

> To prevent abuse, you need to obtain the cookie and course list yourself. The cookie in the source code is just an example.

## Obtain Cookie

Choose one of the following methods:

1. Press F12 in the browser to open the developer tools, select a request in the network tab, and find it in the request headers.
2. Enter `javascript:alert(document.cookie)` in the browser's address bar (case insensitive) ~~(some parts may be eaten by the browser)~~.
3. Use the browser plugin [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm).

## Tips

1. This script is only applicable to pre-selection courses, not for secondary selection.
2. The server resets the session every few hours (currently unclear), so you need to refill the cookie.
3. This version is still in testing. If there are any bugs, please submit an issue.

## Screenshot

![example](example.png)

## Other Features

Explore the source code yourself~ ~~Definitely not because I'm lazy~~.

## Acknowledgements

> Thanks to the following projects for providing inspiration and ideas for this project.

[cqupt-grabber](https://github.com/LgoLgo/cqupt-grabber)

## License

This project uses the GPLv3 license, allowing free use, modification, and distribution of the code, but must comply with the corresponding terms, including crediting the original author and modification content, providing the source code, and maintaining the GPLv3 license, as well as granting contributors the right to use their patents. This project is provided "as is" without any form of warranty. For the full license, please see [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).
