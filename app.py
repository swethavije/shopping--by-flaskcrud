from flask import Flask,render_template,request
import sqlite3 as sql

app = Flask(__name__)

list1=[]
@app.route("/")
def show():
    conn = sql.connect("shop.db")
    cur = conn.cursor()
    cur.execute("select * from buyer")
    a = cur.fetchall()
    for i in a:
        dic ={"name":i[0],"mobile":i[1],"amount":i[2]}
        list1.append(dic)
    return render_template("display.html",data=list1)

list2=[]
@app.route("/product")
def product():
    conn = sql.connect("shop.db")
    cur = conn.cursor()
    cur.execute("select * from product")
    a = cur.fetchall()
    for i in a:
        dic ={"product_name":i[0],"price":i[1]}
        list2.append(dic)
    return render_template("product.html",data=list2)

@app.route("/home",methods=["POST","GET"])
def update():
    if request.form.get("user_name")!=None:
        name=request.form.get("user_name")
        mobile=request.form.get("mobile_number")
        product=request.form.get("product_name")
        quantity=request.form.get("quantity")
        conn = sql.connect("shop.db")
        cur = conn.cursor()
        cur.execute("insert into purchase(user_name,mobile_number,product_name,quantity) values (?,?,?,?)",(name,mobile,product,quantity))
        conn.commit()


        cur.execute("select price from product  where product_name=?",(product,))
        minus=cur.fetchall()
        minus=minus[0][0]
        quantity=int(quantity)
        minus=minus*quantity

        cur.execute("update buyer set amount=amount-? where mobile=?",(minus,mobile))
        conn.commit()
        
        list3=[]
        conn=sql.connect("shop.db")
        cur=conn.cursor()
        cur.execute("select * from buyer")
        a=cur.fetchall()
        for i in a:
            dic={"name":i[0],"mobile":i[1],"amount":i[2]}
            list3.append(dic)

        return render_template("display.html",data=list3)
    return render_template("index.html")









if __name__ == "__main__":
    app.run(debug=True)