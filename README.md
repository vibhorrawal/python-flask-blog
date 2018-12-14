# python-flask-blog

### Setup

Run following comands in windows terminal(For Windows 7 and above).

    ```
    
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
    
    python -m venv venv
    
    venv/Scripts/activate
    
    pip install -r requirements.txt
    
    flask db init

    flask db migrate

    flask db upgrade
    
    ```

### Run Project

    In first terminal
    ```

    python -m smtpd -n -c DebuggingServer localhost:8025

    ```

    In second Terminal
    ```

    flask run

    ```

### Web Link 

[Umhera Flask](https://umhera-flask.herokuapp.com/index)