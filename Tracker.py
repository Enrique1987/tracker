from tkinter import *
from tkinter import messagebox
import sqlite3
import requests
from bs4 import BeautifulSoup
import smtplib

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

#URL = 'https://www.amazon.de/Unicorn-Project-Developers-Disruption-Thriving/dp/1942788762/ref=pd_ys_c_rfy_186606_0?_encoding=UTF8&pd_rd_i=1942788762&pd_rd_r=0XD62VZM3E2D6M9EKGPF&pd_rd_w=ivmkE&pd_rd_wg=b2MD7&pf_rd_p=b590e2fb-7f7b-462f-b256-26d8215ddf09&pf_rd_r=0XD62VZM3E2D6M9EKGPF&psc=1&refRID=9YSKF6ZPD9E20X0XCZ1Z'


#--------------------funciones--------------------------------------

def conexionBBDD():


		miConexion=sqlite3.connect("Elementos")

		miCursor=miConexion.cursor()

		try:
				miCursor.execute('''
					CREATE TABLE  TRACKER 
					(
					ID INTEGER PRIMARY KEY AUTOINCREMENT,
					MESSAGE INTEGER DEFAULT 0,
					NAME  VARCHAR(50) ,
					LINK VARCHAR(250) ,
					PRICE REAL, 
					COMMENT VARCHAR(100))

					''')
				messagebox.showinfo("BBDD","BBDD created succesfully")

				miConexion.commit()


		except:

				messagebox.showwarning("! Atention"," the bbd already exists")


def ExitApp():

	value= messagebox.askquestion("salir", "do you want to exit ?")

	if value=="yes":
			root.destroy()

def cleanFields():

		miName.set("")
		miLink.set("")
		miPrice.set("")
		textoComment.delete(1.0,END)

def create():
	miConexion=sqlite3.connect("Elementos")

	miCursor=miConexion.cursor()

	miCursor.execute("INSERT INTO TRACKER VALUES (NULL,NULL, '" + miName.get() +

			"','" +miLink.get() +
			"','" +miPrice.get() +
			"','" +textoComment.get("1.0", END) + "')")

	miConexion.commit()

	messagebox.showinfo(" BBDD","record inserted succesfully ")
	cleanFields()

def read():

	miConexion=sqlite3.connect("Elementos")

	miCursor=miConexion.cursor()

	try:
		miCursor.execute("SELECT * FROM TRACKER WHERE NAME='" + miName.get()+"'")
		linksToTrack=miCursor.fetchall()

		if linksToTrack is None:
			messagebox.showwarning("! Atention","you need to insert a valid Name ")
		else:
				for elements in linksToTrack:
						
					#miId.set(elements[0])
					miName.set(elements[1])
					miLink.set(elements[2])
					miPrice.set(elements[3])
					textoComment.insert(1.0,elements[4])

				miConexion.commit()
    
	except:		
    		
    		messagebox.showwarning("! Atencion","to read the info you need to insert a valid name ")

def update():

	miConexion=sqlite3.connect("Elementos")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute("UPDATE TRACKER SET NAME='" + miName.get() +
							"',LINK = '" + miLink.get() +
							"',PRICE = '" + miPrice.get() +
							"',COMENTARIOS = '" + textoComment.get("1.0", END) +	
    					 "' WHERE NAME=" + miName.get() )
		miConexion.commit()
		messagebox.showinfo("User","record succesfully update")

	except:		
    		
    		messagebox.showwarning("! Atentio","to make the update you need a valid name")

def delete():

	miConexion=sqlite3.connect("Elementos")

	miCursor=miConexion.cursor()

	try:
		miCursor.execute("DELETE FROM TRACKER WHERE NAME=" + miName.get() )
		miConexion.commit()
		messagebox.showinfo("Link","record succesfully delete")

	except:		
    		
    		messagebox.showwarning("! Atention","to delete the record you need a valid Name")



#check encoder
# print(soup.prettify().encode('utf-8'))
def check_price():

	page = requests.get(miLink.get(),headers=headers)
	encoding = page.encoding if 'charset' in page.headers.get('content-type', '').lower() else None
	soup = BeautifulSoup(page.content, from_encoding=encoding,features="lxml")             # the new parametes to soup.                  
	price = soup.find("span",class_="a-size-base a-color-price a-color-price").get_text()
	article = soup.find("span", id="productTitle").get_text()

	converted_price=float(price_2decimals(price))

	
	if (converted_price < float(miPrice.get())):
		messagebox.showinfo("Name","The article {} hat already the desire price".miName.get())
		send_mail(converted_price,article)

	else:
		messagebox.showinfo("Name","the article is not already to the desired price, we will continue checking it")

def price_2decimals(price):
	price_aux=price
	#find the first digit avoiding situations like price = "n/      34455,22 &shhb€" and take 2 decimals
	for i, c in enumerate(price_aux):
	    if c.isdigit():
	        firstDigit = i
	        break
	coma=price_aux.find(",")+3
	return price_aux[firstDigit:coma].replace(",",".")

#to send email you need enable 2 steps verification

def send_mail(price,article):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('enriquetest1987@gmail.com','xwydfkcfscavgkla')
	subject = "the price the article  fell down! "
	body="the price of {} in wich you were interested fell downe the price is now {} check the amazon link {}".format(article,price,miLink.get())

	msg= f"Subject: {subject}\n\n{body}"
	server.sendmail('enriquebenito87@gmail.com','enriquebenito1987@gmail.com',msg)
	print("heyy email was sended")
	server.quit()



#-------------------------------- End funktions --------------------------#

root=Tk()

barraMenu=Menu(root)
root.config(menu=barraMenu,width=300,height=300)

bbddMenu=Menu(barraMenu,tearoff=0)
bbddMenu.add_command(label="Connect",command=conexionBBDD)
bbddMenu.add_command(label="Exit",command=ExitApp)


barraMenu.add_cascade(label="BBDD",menu=bbddMenu)




#----------------- cominzo de campos ----------------------------#

miFrame=Frame(root)
miFrame.pack()



miId=StringVar()
miName=StringVar()
miPrice=StringVar()
miLink=StringVar()


cuadroName=Entry(miFrame,textvariable=miName)
cuadroName.grid(row=1,column=1,padx=10,pady=10)
cuadroName.config(justify="right")

cuadroLink=Entry(miFrame,textvariable=miLink)
cuadroLink.grid(row=2,column=1,padx=20,pady=10)
cuadroLink.config(justify="right")

cuadroPrice=Entry(miFrame,textvariable=miPrice)
cuadroPrice.grid(row=3,column=1,padx=10,pady=10)
cuadroPrice.config(justify="right")


textoComment=Text(miFrame,width=16,height=5)
textoComment.grid(row=4,column=1,padx=10,pady=10)
scrollVert=Scrollbar(miFrame,command=textoComment.yview)
scrollVert.grid(row=4,column=2,sticky="nsew")


textoComment.config(yscrollcommand=scrollVert.set)

#-------------------------------------- Texto en campos -------------------- ''

#idLabel=Label(miFrame,text="Id:")
#idLabel.grid(row=0,column=0,sticky="e",padx=10,pady=10)

idLabel=Label(miFrame,text="Object to track:")
idLabel.grid(row=1,column=0,sticky="e",padx=10,pady=10)


idLabel=Label(miFrame,text="Link:")
idLabel.grid(row=2,column=0,sticky="e",padx=10,pady=10)

idLabel=Label(miFrame,text="Desired price:")
idLabel.grid(row=3,column=0,sticky="e",padx=10,pady=10)


idLabel=Label(miFrame,text="Comments:")
idLabel.grid(row=4,column=0,sticky="e",padx=10,pady=10)






#---------------------------------- botones ---------------------------------#

miFrame2=Frame(root)

miFrame2.pack()

botonCrear=Button(miFrame2,text="Create",command=create)
botonCrear.grid(row=1,column=0,sticky="e",padx=10,pady=10)

botonLeer=Button(miFrame2,text="Read",command=read)
botonLeer.grid(row=1,column=1,sticky="e",padx=10,pady=10)


botonActualizar=Button(miFrame2,text="Update",command=update)
botonActualizar.grid(row=1,column=2,sticky="e",padx=10,pady=10)



botonBorrar=Button(miFrame2,text="Delete",command=delete)
botonBorrar.grid(row=1,column=3,sticky="e",padx=10,pady=10)


botonBorrar=Button(miFrame2,text="Track",command=check_price)
botonBorrar.grid(row=2,column=2,sticky="e",padx=10,pady=10)


root.mainloop()