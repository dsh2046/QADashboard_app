#!/usr/bin/python
import psycopg2

username = "user1"
conn = psycopg2.connect(database=username, user="postgres", password="12345678", host="10.10.30.250", port="5432")
cur = conn.cursor()


