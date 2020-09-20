#!/usr/bin/python3

# The Magi
# Sabi. Simple, Lightweight, but Not Beautiful

import os, shutil, sys, random

version = "0.10"

startPort = 9000

cwd = os.path.abspath(os.path.dirname(__file__))

imageFormats = ['.jpg', 'jpeg', '.bmp', '.gif', '.png']
videoFormats = ['.mp4', '.mov', '.mkv', '.avi', 'mpeg', 'webm']

html_only = False

def setup(version):
    update = False

    # Check if running as root/sudo
    if not html_only:
        if not os.geteuid() == 0:
            sys.exit('This script must be run as root!')

    # Check if Python 3
    if not sys.version_info[0] == 3:
        sys.exit('This script is only compatible with Python 3.')

    # Check if not Windows
    if os.name != "nt":

    # Check for apt compatibility
        if shutil.which('apt-get'):

    # Check if nginx is installed
            if not shutil.which('nginx'):
                os.system('apt-get update && apt-get install nginx -y')
                update = True

    # Check if apache2 is installed
            if not shutil.which('apache2'):
                if update == True:
                    os.system('apt-get install apache2 -y')
                else:
                    os.system('apt-get update && apt-get install apache2 -y')

    # Check if apache2 directory is present, since it doesn't always create...... >:(
            if not os.path.exists('/etc/apache2'):
                os.makedirs('/etc/apache2')

    # Check if nginx is installed
        if not shutil.which('nginx'):
            sys.exit('nginx is not installed on this machine.\nPlease install nginx if you want to host webservers on this machine,\nor if you just want the webfiles run with the --html-only option.')

    # Check if apache2-utils is installed (for htpasswd authentication)
        if not shutil.which('apache2'):
            print("NOTICE: apache2 is not installed. You will not be able to secure your webpages with a password until you install.\n")

    # Initialize any new webservers
    configs = os.listdir(cwd + "/config")
    for server in os.listdir(cwd + "/categories"):
        if server+".conf" not in configs:
            with open(cwd + "/config/" + server + ".conf", "w") as conf:
                conf.write("category = " + server + "\ntitle = " + server + "\nbanner = " + server + "\nauth = False\n")
        server = cwd + "/categories/" + server
        if "subcategories" not in os.listdir(server):
            os.makedirs(server + "/subcategories")
            for item in os.listdir(server):
                if item != "subcategories":
                    shutil.move(server + "/" + item, server + "/subcategories")
        if "web" not in os.listdir(server):
            os.makedirs(server + "/web")

    # Ensure style directory exists
    if "style" not in os.listdir(cwd):
        os.makedirs(cwd + "/style")
        # TODO Make this Windows/Mac compatible

    # Ensure default style exists
    if not os.path.isfile(cwd + "/style/default.css"):
        defaultCSS()


def defaultCSS():
    with open(cwd + "/style/default.css","w") as css:
        css.write("/*\nSabi. Simple, Lightweight, but Not Beautiful\nhttps://github.com/sabi\n\nTheme: magi-darkmode-default.css\nVersion: 1\n*/\n\n")
        css.write("#background {\n\tbackground-color:#353535;\n\tcolor: white;\n\tmax-width: 800px;\n\tmargin: auto;\n}\n\n")
        css.write(".gallery {\n\tmargin: 5px;\n\tborder: 1px solid #ccc;\n\tfloat: left;\n\twidth: 180px;\n\theight: 200px;\n\toverflow: hidden;\n}\n\n")
        css.write(".gallery:hover {\n\tborder: 1px solid #777;\n}\n\n")
        css.write(".gallery img {\n\twidth: 100%;\n\theight: auto;\n}\n\n")
        css.write(".galleryVideo {\n\tmax-width: 180px;\n\twidth: auto;\n}\n\n")
        css.write(".caption {\n\tdisplay: block;\n\ttext-align: center;\n\tfont-weight: bold;\n}")


def html(category, title, banner, version, style):
    web = os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + "/web/"
    styleDir = os.path.abspath(os.path.dirname(__file__)) + "/style/"
    subcategories = os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + "/subcategories"

    header = "<!DOCTYPE HTML>\n<html>\n\n\t<head>\n\t\t<title>" + title + "</title>\n\t\t<link rel='stylesheet' href='/web/style.css'>\n\t\t<metadata charset='utf-8'>\n\t\t<meta name='generator' content='The Magi " + version + "'/>\n\t</head>\n"

    # Create the main index page
    with open(web + "index.html", "w") as index:
        index.write(header)
        index.write("\n\t<body id=background>\n\n\t\t<div>\n")
        index.write("\t\t\t<h1>" + banner + "</h1>\n")
        for subcat in os.listdir(subcategories):
            index.write('\t\t\t\t<div class="gallery">\n')
            index.write('\t\t\t\t\t<span class="caption">' + subcat + '</span>\n')
            index.write('\t\t\t\t\t<a target="_self" href="/web/' + subcat + '.html">\n')
            while True:
                preview = os.listdir(subcategories + "/" + subcat)[random.randrange(0,len(os.listdir(subcategories + "/" + subcat)))]
                if preview[-4:] in imageFormats:
                    break
            index.write('\t\t\t\t\t\t<img src="/subcategories/' + subcat + '/' + preview + '" alt="' + subcat + '">\n\t\t\t\t\t</a>\n\t\t\t\t</div>\n\n')

            # Create the subcategory pages
            with open(web + subcat + ".html", "w") as subindex:
                subindex.write(header)
                subindex.write("\n\t<body id='background'>\n\n\t\t<h1>" + subcat + "</h1>\n\n")

                # Write all images to top of webpage
                for media in os.listdir(subcategories + "/" + subcat):
                    if media[-4:].lower() in imageFormats:
                        subindex.write('\t\t<div class="gallery">\n')
                        subindex.write('\t\t\t<a target="_self" href="/subcategories/' + subcat + '/' + media + '">\n')
                        subindex.write('\t\t\t\t<img src="/subcategories/' + subcat + '/' + media + '" alt="' + media + '"\n\t\t\t</a>\n\t\t</div>\n\n')

                # Write all videos to end of webpage
                for media in os.listdir(subcategories + "/" + subcat):
                    if media[-4:].lower() in videoFormats:
                        subindex.write('\t\t<div class="gallery">\n')
                        subindex.write('\t\t\t<a target="_self" href="/subcategories/' + subcat + '/' + media + '">\n')
                        subindex.write('\t\t\t\t<video class="galleryVideo" controls="controls" preload="metadata"><source src="/subcategories/' + subcat + '/' + media + '"></video>\n\t\t\t</a>\n\t\t</div>\n\n')


                # Close and save subcategory page
                subindex.write("\t</body>")
                subindex.close()

        # Close and save main index page
        index.write("\t\t</div>\n\t</body>")
        index.close()

        # Copy stylesheet
        shutil.copy(styleDir + style + ".css", web + "style.css")

def readConfig(startPort):
    cwd = os.path.abspath(os.path.dirname(__file__)) + "/config/"
    i = 1
    bigDict = {}
    ports = []
    change = False
    for conf in os.listdir(cwd):
        bigDict[i] = {}
        with open(cwd + conf, "r") as config:
            for line in config.readlines():
                line = line.split(" = ")
                bigDict[i][line[0]] = line[1].strip()

            # Check if port is provided and ensure no collisions
            if "port" in bigDict[i].keys() and bigDict[i]["port"] in ports:
                port = startPort
                while str(port) in ports:
                    port += 1
                bigDict[i]["port"] = str(port)
                print("NOTICE: " + bigDict[i]["category"] + "'s port number had to be change due to overlap. Hosted port is: " + str(port))
                change = True

            # Provide a port if no port is set
            if "port" not in bigDict[i].keys():
                port = startPort
                while str(port) in ports:
                    port += 1
                bigDict[i]["port"] = str(port)

            # Check if authentication is set (True/False/Unique)
            if "auth" not in bigDict[i].keys():
                bigDict[i]["auth"] = "False"

            # Check if a theme/style is set
            if "style" not in bigDict[i].keys():
                bigDict[i]["style"] = "default"
                change = True
            if bigDict[i]["style"][-4:] == ".css":
                bigDict[i]["style"] = bigDict[i]["style"][:-4]

            # Update port mapping
            ports.append(bigDict[i]["port"])

        # If there was outdate info, update the config
        if change == True:
            change = False
            with open(cwd + conf, "w") as config:
                config.write("category = " + bigDict[i]["category"] + "\n")
                config.write("title = " + bigDict[i]["title"] + "\n")
                config.write("banner = " + bigDict[i]["banner"] + "\n")
                config.write("auth = " + bigDict[i]["auth"] + "\n")
                config.write("port = " + bigDict[i]["port"] + "\n")
                config.write("style = " + bigDict[i]["style"] + "\n")
        i+=1
    return bigDict

def authentication(auth, port, category, x):
    trueValues = [True, "true", "t"]
    falseValues = [False, "false", "f"]
    global authSet

    if auth.lower() in trueValues and authSet == False:
        user = input("Enter Username for authentication for private Magi servers.\n")
        os.system("htpasswd -c /etc/apache2/.htpasswd_magi " + user)
        authSet = True

    # if this is the first server in the update or not
    if x == 1:
        f = open("/etc/nginx/sites-enabled/magi","w")
    else:
        f = open("/etc/nginx/sites-enabled/magi","a")

    if auth.lower() == "unique":
        print("\n\n" + "#"*36 + "\n#### AUTHENTICATION CREDENTIALS ####\n" + "#"*36 + "\n")
        user = input("Enter Username for authentication for " + category + "\n")
        f.write("server {\nlisten " + port + ";\nroot " + os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + ";\nindex web/index.html;\nserver_name _;\nauth_basic 'Magi Login';\nauth_basic_user_file /etc/apache2/.htpasswd_" + category + ";\nlocation / {\n}\n}")
        os.system("htpasswd -c /etc/apache2/.htpasswd_" + category + " " + user)

    elif auth.lower() in trueValues:
        f.write("server {\nlisten " + port + ";\nroot " + os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + ";\nindex web/index.html;\nserver_name _;\nauth_basic 'Magi Login';\nauth_basic_user_file /etc/apache2/.htpasswd_magi;\nlocation / {\n}\n}")

    elif auth.lower() in falseValues:
        print("No authentication requested for: " + category)
        f.write("server {\nlisten " + port + ";\nroot " + os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + ";\nindex web/index.html;\nserver_name _;\nlocation / {\n}\n}")
    f.close()

def end(ports):
    with open(os.path.abspath(os.path.dirname(__file__)) + "/docs/myWebservers.txt","w") as myWebservers:
        myWebservers.write("The Magi by Sabi\n")
        for k, v in ports.items():
            msg = k + " is hosted on: " + v
            print(msg)
            myWebservers.write(msg + "\n")
    myWebservers.close()

    # Change permissions
    os.system("for i in $(ls /home); do usermod -aG www-data $i; done")
    os.system("chown -R www-data:www-data " + cwd)
    os.system("chmod -R 777 " + cwd)

    os.system("systemctl restart nginx")

def changelog():
    sys.exit("""The Magi by Sabi. Simple, Lightweight, but Not Beautiful.
    0.10 - Created mapping for starting port for easy configurations
    0.09 - Permissions change, style changes
    0.08 - External CSS support, improved formatting, added changelog, bug fixes
    0.07 - Redirect due to incompatibility issues with HTML Only Mode
    0.06 - Added HTML Only mode, Version Tracking, bug fixes
    """)


#################
# Start Program #
#################

# Check for options flags
if len(sys.argv) > 1:
    if sys.argv[1] in ["-h","--help"]:
        sys.exit("""The Magi by Sabi. Simple, Lightweight, but Not Beautiful.
        -h  --help       : Display this menu
        -v  --version    : Display the version number
        -s  --servers    : Print list of current servers
        -H  --html-only  : Generate html files without changing the nginx webserver backend
        -cl --changelog  : Print changes to The Magi
        """)
    elif sys.argv[1] in ["-v","--version"]:
        sys.exit(version)
    elif sys.argv[1] in ["-s", "--servers"]:
        with open("docs/myWebservers.txt", "r") as myWebservers:
            currentServers = myWebservers.read()
        sys.exit(currentServers)
    elif sys.argv[1] in ["-H","--html-only"]:
        html_only = True
    elif sys.argv[1] in ["-cl","--changelog"]:
        changelog()
    else:
        sys.exit(sys.argv[1] + " is not a valid option. See -h or --help for list of options.")

ports = {}
authSet = False

# Check if Windows
if os.name == "nt":
    sys.exit("The Magi is currently only compatible with Linux")
    #html_only = True

# Warn HTML Only mode
if html_only == True:
    print("The Magi will generate HTML files only. Check the README for info about hosting with The Magi")

# Check dependencies and new Magi webservers
setup(version)

# Read configuration files and add them to bigDict
bigDict = readConfig(startPort)

# Prime variables for each webserver
for x in bigDict.keys():
    auth = bigDict[x]["auth"]
    port = bigDict[x]["port"]
    category = bigDict[x]["category"]
    title = bigDict[x]["title"]
    banner = bigDict[x]["banner"]
    style = bigDict[x]["style"]
    ports[category] = port

# Create the nginx configuration file
    if not html_only:
        authentication(auth, port, category, x)

# Create the html files
    html(category, title, banner, version, style)

# Print a mapping of all webservers and ports and save to docs/myWebservers.txt
if not html_only:
    end(ports)

print("The Magi has updated!")
