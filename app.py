import datetime
import os
from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()  

def create_app():
        app=Flask(__name__)

        client=MongoClient(os.getenv("MONGODB_URI"))
        app.db=client.Microblog

        @app.route("/",methods=["GET","POST"])
        def index():
            if request.method=="POST":
                blog_content=request.form.get("content")
                # print(blog_content)   

                dte=str(datetime.date.today())
                # print(dte)
                params={"content":blog_content,"date":dte}
                app.db.entries.insert_one(params)
                return redirect(url_for('index'))

            recent_entries=[[entry["content"],entry["date"]]  for entry in app.db.entries.find({})]
            print(recent_entries)
            recent_entries.reverse()

            return render_template("index.html",recent_entries=recent_entries)

        if __name__=="__main__":
            app.run(debug=True)
        
        return app