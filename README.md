# RECYCLE TRADE HUB
- This is an online shopping website where anyone can buy, sell or barter recyclable materials

# HOW TO RUN THE WEB APP ONLINE
- Visit the url https://recycletradehub.shahibu.com/

# HOW TO RUN THE WEB APP ON YOUR LOCAL ENVIRONMENT
> # SECTION 1: SETTING UP


## Clone The Project
```bash
    git clone https://github.com/MichelleThuo/Recycle-Trade-Hub.git
```


## CREATE A VIRTUAL ENVIRONMENT

- Windows
    ``` bash
    py -m venv venv
    ```
- Linux 
    ``` bash
    python3 -m venv venv
    ```

## ACTIVATE THE VIRTUAL ENVIRONMENT
- Windows
    ``` bash
    ./venv/Scripts/activate
    ```
- Linux
    ```
    source venv/bin/activate
    ```
## INSTALL THE REQUIREMENTS
``` bash
pip install -r requirements.txt
```

## NAVIGATE TO THE PROJECT FOLDER
``` bash
cd Recycle-Trade-Hub
```

## CREATE SUPERUSER
- Windows
    ```
    python3 -m manage createsuperuser
    ```
- Linux
    ```
    py -m manage createsuperuser
    ```
-----------
> # SECTION 2: RUN SERVER
-----------

- Windows
    ``` bash
    py -m manage runserver
    ```
- Linux
    ``` bash
    python3 -m manage runserver
    ```

> IF YOU ARE HERE THEN THAT MEANS EVERYTHING IS WORKING WELL. 

> Open the web app by visiting [http://127.0.0.1:8000](http://127.0.0.1:8000)

> # SECTION 3: HOW IT WORKS
- To login as an admin use the details you entered when creating the superuser.

- To login as a normal user, you have to register your account on the web app first.



