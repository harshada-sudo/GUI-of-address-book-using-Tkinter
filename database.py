import tkinter as tk
from PIL import ImageTk,Image
import sqlite3

root=tk.Tk()
root.title("Harshada")
root.geometry("350x400")

#database


'''
cursor.execute("""
CREATE TABLE addresses(
firstname VARCHAR(20),
lastname VARCHAR(20),
address VARCHAR(20),
city VARCHAR(20),
zipcode integer
);
""")    
'''

#create update function
def save():
    with sqlite3.connect("address_book.db") as db:
        cursor=db.cursor()

    record_id=delete_box.get()
    cursor.execute("""
    UPDATE addresses SET
    firstname = :f_name,
    lastname = :l_name,
    address = :address_d,
    city = :city_d,
    zipcode = :zipcode_d

    WHERE oid= :oid""",
    {
        'f_name' : f_name_update.get(),
        'l_name' : l_name_update.get(),
        'address_d' : address_update.get(),
        'city_d' : city_update.get(),
        'zipcode_d' : zipcode_update.get(),
        'oid' : record_id
    })

    db.commit()

    editor.destroy()

def update():
    global editor
    editor=tk.Tk()
    editor.title("Update a Record")
    editor.geometry("350x400")

    with sqlite3.connect("address_book.db") as db:
        cursor=db.cursor()

    cursor.execute("SELECT * FROM addresses WHERE oid = " + delete_box.get())
    record=cursor.fetchall()

    global f_name_update
    global l_name_update
    global address_update
    global city_update
    global zipcode_update

    #textbox
    f_name_update=tk.Entry(editor,width=30)
    f_name_update.grid(row=0,column=1,padx=10,pady=(15,0))
    l_name_update=tk.Entry(editor,width=30)
    l_name_update.grid(row=1,column=1,padx=10)
    address_update=tk.Entry(editor,width=30)
    address_update.grid(row=2,column=1,padx=10)
    city_update=tk.Entry(editor,width=30)
    city_update.grid(row=3,column=1,padx=10)
    zipcode_update=tk.Entry(editor,width=30)
    zipcode_update.grid(row=4,column=1,padx=10)
    
    #create label field
    first_name_label=tk.Label(editor,text="First Name",font=("times new roman",10,"bold"))
    first_name_label.grid(row=0,column=0,pady=(15,0))
    last_name_label=tk.Label(editor,text="Last Name",font=("times new roman",10,"bold"))
    last_name_label.grid(row=1,column=0)
    Address_label=tk.Label(editor,text="Address",font=("times new roman",10,"bold"))
    Address_label.grid(row=2,column=0)
    city_label=tk.Label(editor,text="City",font=("times new roman",10,"bold"))
    city_label.grid(row=3,column=0)
    zipcode_label=tk.Label(editor,text="Zipcode",font=("times new roman",10,"bold"))
    zipcode_label.grid(row=4,column=0)
    
    #insert original records in textbox to change them
    for i in record:
        f_name_update.insert(0,i[0])
        l_name_update.insert(0,i[1])
        address_update.insert(0,i[2])
        city_update.insert(0,i[3])
        zipcode_update.insert(0,i[4])  
    
    #button for save changes 
    save_change_btn=tk.Button(editor,text="Save changes",command=save)
    save_change_btn.grid(row=5,column=0,columnspan=2,padx=10,pady=10,ipadx=120)

    db.commit()

#create delete function
def delete():
    with sqlite3.connect("address_book.db") as db:
        cursor=db.cursor()

    cursor.execute("DELETE from addresses WHERE oid ="+delete_box.get())
    delete_box.delete(0,tk.END)
    db.commit()

#create submit function
def submit():
    with sqlite3.connect("address_book.db") as db:
        cursor=db.cursor()
    
    #insert data into table
    cursor.execute("INSERT INTO addresses VALUES(:f_name,:l_name,:address,:city,:zipcode)",
        {
            'f_name':f_name.get(),
            'l_name':l_name.get(),
            'address':address.get(),
            'city':city.get(),
            'zipcode':zipcode.get()
        }
    )

    db.commit()

    f_name.delete(0,tk.END)
    l_name.delete(0,tk.END)
    address.delete(0,tk.END)
    city.delete(0,tk.END)
    zipcode.delete(0,tk.END)

#create show function
def show():
    with sqlite3.connect("address_book.db") as db:
        cursor=db.cursor()

    cursor.execute("SELECT *,oid FROM addresses")
    record=cursor.fetchall()
    print(record)

    print_r=''
    for i in record:
        print_r +=str(i[0])+" "+str(i[1])+" "+"\t"+str(i[5])+"\n"

    record_lbl=tk.Label(root,text=print_r)
    record_lbl.grid(row=10,column=0,columnspan=2)

    db.commit()
#create textboxes
f_name=tk.Entry(root,width=30)
f_name.grid(row=0,column=1,padx=10,pady=(15,0))
l_name=tk.Entry(root,width=30)
l_name.grid(row=1,column=1,padx=10)
address=tk.Entry(root,width=30)
address.grid(row=2,column=1,padx=10)
city=tk.Entry(root,width=30)
city.grid(row=3,column=1,padx=10)
zipcode=tk.Entry(root,width=30)
zipcode.grid(row=4,column=1,padx=10)
delete_box=tk.Entry(root,width=30)
delete_box.grid(row=7,column=1,pady=5)

#create label field
first_name_label=tk.Label(root,text="First Name",font=("times new roman",10,"bold"))
first_name_label.grid(row=0,column=0,pady=(15,0))
last_name_label=tk.Label(root,text="Last Name",font=("times new roman",10,"bold"))
last_name_label.grid(row=1,column=0)
Address_label=tk.Label(root,text="Address",font=("times new roman",10,"bold"))
Address_label.grid(row=2,column=0)
city_label=tk.Label(root,text="City",font=("times new roman",10,"bold"))
city_label.grid(row=3,column=0)
zipcode_label=tk.Label(root,text="Zipcode",font=("times new roman",10,"bold"))
zipcode_label.grid(row=4,column=0)
delete_box_lbl=tk.Label(root,text="Delete ID  :",font=("times new roman",10,"bold"))
delete_box_lbl.grid(row=7,column=0,pady=5)

#create submit button
submit_btn=tk.Button(root,text="Add address record",command=submit)
submit_btn.grid(row=5,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

show_btn=tk.Button(root,text="Show record",command=show)
show_btn.grid(row=6,column=0,columnspan=2,padx=10,pady=10,ipadx=120)

delete_btn=tk.Button(root,text="Delete record",command=delete)
delete_btn.grid(row=8,column=0,columnspan=2,padx=10,pady=10,ipadx=120)

update_btn=tk.Button(root,text="Update a record",command=update)
update_btn.grid(row=9,column=0,columnspan=2,padx=10,pady=10,ipadx=114)

root.mainloop()