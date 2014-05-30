---
layout: default
title: General Development Guide
---

This page documents some of our development tools and conventions. It aims to be thorough as possible while
remaining generic. Individual projects then document their own installation and configuration details.

## <a name="Fabric"></a> Fabric

We use Fabric to script deployment tasks. It requires Python 2.7, but is difficult to properly install.

First, [install Python 2.7]({{ site.baseurl }}/development_general.html#Python27), but stop prior to installing `requirements2.txt`.

Fabric generally does not cleanly install from pip. The underlying problem is with installing pycrypto, and is resolved by using a prebuilt binary:

    env27\Scripts\activate.bat
    easy_install http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe

You can now install Fabric:

    env27\Scripts\activate.bat
    pip install fabric

Or your full set of Python 2.7 requirements from `requirements2.txt`.

    env27\Scripts\activate.bat
    pip install -r requirements2.txt

## <a name="Jekyll"></a> Jekyll

We use Jekyll to build our websites. It requires Python 2.7 and Ruby.

First, [install Python 2.7]({{ site.baseurl }}/development_general.html#Python27).

Second, [install Ruby]({{ site.baseurl }}/development_general.html#Ruby).

Now we can install Jekyll:

    gem install jekyll

By convention, we use Jekyll to ease deployment.

First, [install Fabric]({{ site.baseurl }}/development_general.html#Fabric).

The `serve` task will then continuously and serve the website on `localhost:4000`.

    fab serve

The `deploy` task will deploy the site to its production location.

    fab deploy

## <a name="Node.js"></a> Node.js

### Microsoft Visual Studio C++ 2012 for Windows Desktop

Many Node modules require a C compiler for native code included in the module.

Microsoft Visual Studio C++ 2012 for Windows Desktop is freely available:

<http://go.microsoft.com/?linkid=9816758>

### Node.js

When I first tried to install Node.js, a tree fell on my house. Seriously. So first check you are not under any trees.

You get node here:

<http://nodejs.org/download/>

Unfortunately, the current installers seem to require a reboot for path settings to take effect.

You should then be sure to understand the difference between global and local modules:

<http://blog.nodejs.org/2011/03/23/npm-1-0-global-vs-local-installation/>

Following the advice "install it in both places", we install several modules globally. These each have commands that it is convenient to be able to easily execute.

Cordova/PhoneGap enables mobile applications based on HTML, CSS, and Javascript:

    npm -g install cordova
    npm -g install phonegap

Ionic works with Cordova/PhoneGap and Angular to target mobile apps:

    npm -g install ionic

And you should install a project's local dependencies:

    npm install

## Python

### <a name="MinGW"></a> MinGW

<div class="alert">
{% capture m %}
These instructions for C compiling with Python 3.4 on Windows may be incorrect.

<https://github.com/Fogies/web-jayfo/issues/18>
{% endcapture %}
{{ m | markdownify }}
</div>

Many Python modules require a C compiler for native code included in the module. If you have Microsoft Visual Studio, you may be able to skip this. I am using MinGW:

<http://www.mingw.org/download/installer>

During the install:

  * Ensure Checked "Add GCC to your system PATH"
  * Uncheck "Bind to Python Installations".
  * Ensure Checked "Set the default runtime library to use". Select "MSVCR90.DLL".

Binding MinGW to a Python install involves a few lines in a configuration file. The installer can insert those in your primary Python installations (e.g., `c:\Python27\`), but we should never actually use those installations.  We will instead use Python virtual environments, and discuss binding when configuring those environments.

### <a name="Python27"></a> Python 2.7

We use Python 2.7 as little as possible, but there are still libraries that require it.

First, [install MinGW]({{ site.baseurl }}/development_general.html#MinGW).

You then need Python:

<https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi>

Python 2.7 does not come with a built-in package manager, so we need to install it. Download these two files:

<https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py>

<https://raw.github.com/pypa/pip/master/contrib/get-pip.py>

Then you can install pip:

    c:\Python27\python ez_setup.py
    c:\Python27\python get-pip.py

Now you need virtualenv:

    c:\Python27\Scripts\pip install virtualenv

Finally you can create a Python environment for your project. By convention, we call our environment `env27`:

    c:\Python27\Scripts\virtualenv.exe env27

You bind the environment to your MinGW install by editing `env27\Lib\disutils\distutils.cfg` to include:

    [build]
    compiler=mingw32

Now you can install your project requirements. By convention, we put these in `requirements2.txt`:

    env27\Scripts\activate.bat
    pip install -r requirements2.txt

If a project includes Fabric in its requirements, this install will fail. See [installing Fabric]({{ site.baseurl }}/development_general.html#Fabric).

### <a name="Python34"></a> Python 3.4

<div class="alert">
{% capture m %}
These instructions for C compiling with Python 3.4 on Windows may be incorrect.

<https://github.com/Fogies/web-jayfo/issues/18>
{% endcapture %}
{{ m | markdownify }}
</div>

We should use Python 3 whenever possible. Currently that means Python 3.4.

First, [install MinGW]({{ site.baseurl }}/development_general.html#MinGW).

You then need Python:

<https://www.python.org/ftp/python/3.4.1/python-3.4.1.msi>

Python 3.4 includes pip and pyvenv, so we just get started. By convention, we call our environment `env34`:

    c:\Python34\Tools\Scripts\pyvenv.py env34

You bind the environment to your MinGW install by editing `env34\Lib\disutils\distutils.cfg` to include:

    [build]
    compiler=mingw32

Now you can install your project requirements. By convention, we put these in `requirements3.txt`:

    env34\Scripts\activate.bat
    pip install -r requirements3.txt

## <a name="Ruby"></a> Ruby

To install Ruby, you need Ruby and an associated DevKit. You can get them here:

<http://rubyinstaller.org/downloads/>

Per the recommendations of the Ruby folks, I am using the 1.93 versions. First install Ruby:

<http://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-1.9.3-p545.exe?direct>

During the install:

  * I use the install path `c:\Ruby193`
  * Ensure Checked "Add Ruby executables to your PATH"

Then install the Ruby DevKit:

<https://github.com/downloads/oneclick/rubyinstaller/DevKit-tdm-32-4.5.2-20111229-1559-sfx.exe>

Unzip it to a permanent directory. I use `c:\RubyDevKit`. Then install the DevKit:

    cd c:\RubyDevKit
    ruby dk.rb init
    ruby dk.rb install