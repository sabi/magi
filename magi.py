#!/usr/bin/python3

# The Magi
# Sabi. Simple, Lightweight, but Not Beautiful

import os, shutil, sys, random 

imageFormats = ['.jpg', 'jpeg', '.bmp', '.gif', '.png']
videoFormats = ['.mp4', '.mov', '.mkv', '.avi', 'mpeg', 'webm']

def setup():
    update = False
    cwd = os.path.abspath(os.path.dirname(__file__))
    
    # Check if running as root/sudo
    if not os.geteuid() == 0:
        sys.exit('This script must be run as root!')

    # Check if Python 3
    if not sys.version_info[0] == 3:
        sys.exit('This script is only compatible with Python 3.')
    
    # Check if nginx is installed
    if not os.path.isdir('/etc/nginx'):
        update = True
        os.system("apt-get update && apt-get install nginx -y")
    
    # Check if apache2-utils is installed (for htpasswd authentication)
    if not os.path.isdir('/etc/apache2'):
        if update == False:
            update = True
            os.system("apt-get update")
        os.system("apt-get install apache2-utils -y")
    
    # Check if apache2 directory is present, since it doesn't always create...... >:(
    if not os.path.exists('/etc/apache2'):
        os.makedirs('/etc/apache2')
    
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

def html(category, title, banner):
    web = os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + "/web/"
    subcategories = os.path.abspath(os.path.dirname(__file__)) + "/categories/" + category + "/subcategories"
    
    header = "<!DOCTYPE HTML>\n<html>\n<head>\n<title>" + title + "</title>\n<metadata charset='utf-8'>\n</head>\n"
    style1 = "<style> "
    style2 = "<style>\ndiv.gallery {\n  margin: 5px;\n  border: 1px solid #ccc;\n  float:left;\n  width: 180px;\n}\n\ndiv.gallery:hover {\n border: 1px solid #777;\n}\n\ndiv.gallery img {\n width: 100%;\n  height:auto;\n}\n\n.caption {\n  display: block;\ntext-align: center;\nfont-weight: bold;\n}\n</style>\n"


    # Create the main index page
    with open(web + "index.html", "w") as index:
        index.write(header)
        index.write(style2)
        index.write("<body>")
        index.write("<h1>" + banner + "</h1>\n")
        for subcat in os.listdir(subcategories):
            index.write('<div class="gallery">')
            index.write('<a target="_self" href="/web/' + subcat + '.html">')
            while True:
                preview = os.listdir(subcategories + "/" + subcat)[random.randrange(0,len(os.listdir(subcategories + "/" + subcat)))]
                if preview[-4:] in imageFormats:
                    break
            index.write('<img src="/subcategories/' + subcat + '/' + preview + '" alt="' + subcat + '" height:"100%" width:"auto">\n</a>\n<span class="caption">' + subcat + '</div>\n\n')

            # Create the subcategory pages
            with open(web + subcat + ".html", "w") as subindex:
                subindex.write(header)
                subindex.write(style2)
                subindex.write("<body>\n<h1>" + subcat + "</h1>\n\n")
                
                # Write all images to top of webpage
                for media in os.listdir(subcategories + "/" + subcat):
                    if media[-4:].lower() in imageFormats:
                        subindex.write('<div class="gallery">')
                        subindex.write('<a target="_self" href="/subcategories/' + subcat + '/' + media + '">')
                        subindex.write('<img src="/subcategories/' + subcat + '/' + media + '" alt="' + media + '" height:"100%" width:"auto">\n</a>\n</div>\n\n')
                
                # Write all videos to end of webpage
                for media in os.listdir(subcategories + "/" + subcat):
                    if media[-4:].lower() in videoFormats:
                        subindex.write('<div class="gallery">')
                        subindex.write('<a target="_self" href="/subcategories/' + subcat + '/' + media + '">')
                        subindex.write('<video width="500" controls><source src="/subcategories/' + subcat + '/' + media + '" type="video/mp4"></video>\n</a>\n</div>\n\n')
                

                # Close and save subcategory page
                subindex.write("</body>")
                subindex.close()

        # Close and save main index page
        index.write("</body>")        
        index.close()
    
def readConfig():
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
            if "port" in bigDict[i].keys() and bigDict[i]["port"] in ports:
                port = 9000
                while str(port) in ports:
                    port += 1
                bigDict[i]["port"] = str(port)
                print(bigDict[i]["category"] + "'s port number had to be change due to overlap. Hosted port is: " + str(port))
                change = True
            if "port" not in bigDict[i].keys():
                port = 9000
                while str(port) in ports:
                    port += 1
                bigDict[i]["port"] = str(port)
            if "auth" not in bigDict[i].keys():
                bigDict[i]["auth"] = "False"
            ports.append(bigDict[i]["port"])
            config.close()
            if change == True:
                change == False
                with open(cwd + conf, "w") as config:
                    config.write("category = " + bigDict[i]["category"] + "\n")
                    config.write("title = " + bigDict[i]["title"] + "\n")
                    config.write("banner = " + bigDict[i]["banner"] + "\n")
                    config.write("auth = " + bigDict[i]["auth"] + "\n")
                    config.write("port = " + bigDict[i]["port"] + "\n")
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
        for k, v in ports.items():
            msg = k + " is hosted on: " + v
            print(msg)
            myWebservers.write(msg + "\n")
    myWebservers.close()

    os.system("systemctl restart nginx")
    print("The Magi has updated!")


#################
# Start Program #
#################

ports = {}
authSet = False

# Check dependencies and new Magi webservers
setup()

# Read configuration files and add them to bigDict
bigDict = readConfig()

# Prime variables for each webserver
for x in bigDict.keys():
    auth = bigDict[x]["auth"]
    port = bigDict[x]["port"]
    category = bigDict[x]["category"]
    title = bigDict[x]["title"]
    banner = bigDict[x]["banner"]
    ports[category] = port

# Create the nginx configuration file
    authentication(auth, port, category, x)

# Create the html files
    html(category, title, banner)

# Print a mapping of all webservers and ports and save to docs/myWebservers.txt
end(ports)