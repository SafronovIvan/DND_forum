import psycopg2
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3b0c4429ae41e4649b934c2309867314259802afcdb876dbdce149afbf4c8996fb92427'

def open_DataBase(env_file="bd.end"):
    try:
        load_dotenv(env_file)
        bd = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT'),
            database = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )
        cursor = database.cursor()
        return bd, cursor
            
    except Exception as e:
        print(e)


database, cursor = open_DataBase()