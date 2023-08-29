import os.path
from email.mime.application import MIMEApplication
from tkinter import Button, Frame, Tk, messagebox, Label, simpledialog, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from decouple import config
import database
from database import connect_database, close_database
import mysql.connector


# colors
whitesmoke = "#dcdee8"
whiteBg = "#e6e7eb"
blackLight = "#3d3f47"
blackButLight = "#585959"
blue = "#213ac4"


# Logic
class SalesData:
    """Class to store sales data"""
    def __init__(
        self,
        id,
        name_product,
        cliet,
        valueFrete,
        amount,
        saller,
        form_pag,
        subTotal,
        total,
        email,
    ):
        """Initialize an instance of the SalesData class"""
        self.id = id
        self.name_product = name_product
        self.client = cliet
        self.valueFrete = valueFrete
        self.amount = amount
        self.saller = saller
        self.form_pag = form_pag
        self.subTotal = subTotal
        self.total = total
        self.email = email


def get_inputs_users():
    """Get user input using dialog boxes"""
    id = simpledialog.askstring("Numero de serie do produto", "Numero do Produto: ")
    if id is None:
        return None

    nameProduct = simpledialog.askstring("Nome do produto", "Nome Produto")
    if nameProduct is None:
        return None

    client = simpledialog.askstring("Nome cliente", "Nome do cliente")
    if client is None:
        return None

    valueFrete = simpledialog.askfloat("Valor Frete", "Frete: ")
    if valueFrete is None:
        return None

    amount = simpledialog.askfloat("Quantidade", "Quantidade")
    if amount is None:
        return None

    saller = simpledialog.askstring("Vendedor", "Vendedor")
    if saller is None:
        return None

    form_pag = simpledialog.askstring("Forma de pagamento", "Forma de pagamento")
    if form_pag is None:
        return None

    subTotal = simpledialog.askfloat("SubTotal", "SubTotal: ")
    if subTotal is None:
        return None

    total = simpledialog.askfloat("Total", "Total: ")
    if total is None:
        return None

    email = simpledialog.askstring("Email", "Email")
    if email is None:
        return None

    sales_data = SalesData(
        id,
        nameProduct,
        client,
        valueFrete,
        amount,
        saller,
        form_pag,
        subTotal,
        total,
        email,
    )
    return sales_data


def insert_customers(name, email):
    bank = database.connect_database()
    if bank is not None:
        try:
            cursor = bank.cursor()

            insert_query = "INSERT INTO customers (name, email) VALUES (%s, %s)"
            data_tuple = (name, email)
            cursor.execute(insert_query, data_tuple)
            customer_id = cursor.lastrowid
            bank.commit()
            cursor.close()
            database.close_database(bank)

            return customer_id

        except mysql.connector.Error as err:
            print("Erro durante a inserção na tabela de clientes:", err)
            bank.rollback()

    return None


def insert_product(name, price):
    bank = database.connect_database()
    if bank is not None:
        try:
            cursor = bank.cursor()

            insert_query = "INSERT INTO products (name, price) VALUES (%s, %s)"
            data_tuple = (name, price)
            cursor.execute(insert_query, data_tuple)
            product_id = cursor.lastrowid
            bank.commit()
            cursor.close()
            database.close_database(bank)

            return product_id

        except mysql.connector.Error as err:
            print("Erro durante a inserção na tabela de produtos:", err)
            bank.rollback()

    return None


def insert_sales(sales_data, product_id, customer_id):
    bank = database.connect_database()
    if bank is not None:
        try:
            cursor = bank.cursor()

            # Prepare the INSERT INTO statement
            insert_query = "INSERT INTO sales (amount, valueFreight, date_created, subtotal, total, form_payment, product_id, customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data_tuple = (
                sales_data.amount,
                sales_data.valueFrete,
                date_now,
                sales_data.subTotal,
                sales_data.total,
                sales_data.form_pag,
                product_id,
                customer_id,
            )
            cursor.execute(insert_query, data_tuple)
            bank.commit()
            cursor.close()
            database.close_database(bank)

            statusGenereted.config(text="Produto autorizado com sucesso")

        except mysql.connector.Error as err:
            print("Erro durante a inserção no banco de dados:", err)
            statusGenereted.config(text=f"Erro no banco de dados: {err}")
            bank.rollback()

def generate_invoice_pdf(sales_data):

    pdf_filename = f'arquivo_{sales_data.id}.pdf'

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, "NOTA FISCAL\n\n")
    c.drawString(100, 730, f'Venda ID: {sales_data.id}')
    c.drawString(100, 710, f'Produto: {sales_data.name_product}')
    c.drawString(100, 690, f'Frete: {sales_data.valueFrete}')
    c.drawString(100, 670, f'Quantidade de produtos: {sales_data.amount}')
    c.drawString(100, 650, f'SubTotal: R$ {sales_data.subTotal:.2f}')
    c.drawString(100, 630, f'Total: R$ {sales_data.total:.2f}')
    c.drawString(100, 610, f'Vendedor: {sales_data.saller}')
    c.drawString(100, 590, f'Forma De pagamento: {sales_data.form_pag}')
    c.drawString(100, 570, f'Nome Cliente: {sales_data.client}')

    c.save()

    return pdf_filename

def generate_and_save_pdf(sales_data):
    """Generate and save the PDF invoice"""
    pdf_filename = generate_invoice_pdf(sales_data)

    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Salvar Nota Fiscal"
    )

    if (save_path):
        import shutil
        shutil.move(pdf_filename, save_path)
        messagebox.showinfo("Sucesso", f"Arquivo {save_path} salvo com sucesso!")

def handleNew():
    """Handle creation of new sales and calculate discounts"""
    sales_data = get_inputs_users()

    if sales_data is None:
        statusGenereted.config(text="Erro: Informações incorretas ou vazias.")
        return

    generate_invoice_pdf(sales_data)

    numberGenerated.config(text=sales_data.id)
    nameProductGenereted.config(text=sales_data.name_product)
    valueFreightGenereted.config(text=f"{sales_data.valueFrete}R$")
    amountGenereted.config(text=sales_data.amount)
    subTotalGenereted.config(text=sales_data.subTotal)
    totalGenereted.config(text=sales_data.total)
    salesGenered.config(text=sales_data.saller)
    formPaymentGenereted.config(text=sales_data.form_pag)
    clientGenereted.config(text=sales_data.client)

    # Value conversion
    freight_value = float(sales_data.valueFrete)
    subTotal_value = float(sales_data.subTotal)
    amount_value = float(sales_data.amount)

    discount_value = 0.0  # Defining a default value
    isDiscount_applied = False

    if sales_data.total < 100:
        messagebox.showinfo(
            "Desconto no frete", "Parabens voce ganhou 10% de desconto no frete."
        )
        newValueFreight = 30 - (30 * 0.30)
        valueFreightGenereted.config(text=f"{newValueFreight:.2f}R$")
        isDiscount_applied = True

    if amount_value >= 4:
        messagebox.showinfo(
            "Desconto",
            "Parabens voce ganhou 10% de desconto. Na compra de mais 5 itens o desconto dobra.",
        )
        newTotal = sales_data.total - (sales_data.total * 0.10)
        discount_value = 0.10
        totalGenereted.config(text=f"{newTotal:.2f}")
        subTotalGenereted.config(text=f"{newTotal:.2f}")
        discountGenereted.config(text=f"{discount_value * 100:.0f}%")
        isDiscount_applied = True

        if isDiscount_applied:
            statusGenereted.config(text=f"Produto autorizado descontos")
            return
        else:
            statusGenereted.config(text=f"Produto autorizado com sucesso")

    if sales_data is None:
        statusGenereted.config(text="Erro: Informações incorretas ou vazias.")
        return

    product_id = insert_product(sales_data.name_product, sales_data.total)
    customer_id = insert_customers(sales_data.client, sales_data.email)

    if product_id is None:
        messagebox.showinfo("Erro", "Erro ao inserir o produto")

    if customer_id is None:
        messagebox.showinfo("Erro", "Erro ao inserir o cliente")

    insert_sales(sales_data, product_id, customer_id)

    return sales_data

date_now = datetime.now()
date_formated = date_now.strftime("%Y-%m-%d")

window = Tk()
window.resizable(False, False)
window.geometry("800x400")
window.configure(background=whiteBg)
window.title("")

# frames
frame_top = Frame(
    window,
    height=53,
    width=780,
    bg=whitesmoke,
    highlightbackground=blackButLight,
    highlightthickness=2,
)
frame_top.grid(row=1, column=0, padx=2, pady=10)

#  --------------- #

frame_middle = Frame(
    window,
    height=290,
    width=780,
    bg=whitesmoke,
)
frame_middle.grid(
    row=2,
    column=0,
)

#  ------Buttons--------- #


# Buttons the left
btn_new = Button(
    frame_top,
    text="Novo".upper(),
    font=("Arial 11 bold"),
    width=5,
    highlightbackground=blackLight,
    highlightthickness=2,
    command=handleNew,
)
btn_new.place(
    x=15,
    y=10,
)

btn_save = Button(
    frame_top,
    text="Salvar".upper(),
    font=("Arial 11 bold"),
    width=7,
    highlightbackground=blackLight,
    highlightthickness=2
)
btn_save.place(
    x=79,
    y=10,
)

btn_quit = Button(
    frame_top,
    text="Fechar".upper(),
    font=("Arial 11 bold"),
    highlightbackground=blackLight,
    highlightthickness=2,
    width=20,
)
btn_quit.place(
    x=550,
    y=10,
)

# Front end middle

# labels / widget / buttons the left

nameProduct = Label(
    frame_middle, text="Nome do Produto: ", font=("Arial 10 bold"), bg=whitesmoke
)

nameProduct.place(
    x=20,
    y=20,
)

nameProductGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
nameProductGenereted.place(
    x=150,
    y=20,
)


number = Label(frame_middle, text="Número: ", font=("Arial 10 bold"), bg=whitesmoke)

number.place(
    x=20,
    y=60,
)

numberGenerated = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
numberGenerated.place(
    x=150,
    y=60,
)

status = Label(
    frame_middle,
    text="Status:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
status.place(
    x=20,
    y=100,
)

statusGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
statusGenereted.place(
    x=150,
    y=100,
)

client = Label(
    frame_middle,
    text="Cliente:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
client.place(
    x=20,
    y=140,
)

clientGenereted = Label(
    frame_middle,
    text="XXXXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
clientGenereted.place(
    x=150,
    y=140,
)

valueFreight = Label(
    frame_middle,
    text="Valor do frete:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
valueFreight.place(
    x=20,
    y=180,
)

valueFreightGenereted = Label(
    frame_middle,
    text="Frete gerado",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
valueFreightGenereted.place(
    x=150,
    y=180,
)

discount = Label(
    frame_middle,
    text="Valor Desconto:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
discount.place(
    x=20,
    y=220,
)

discountGenereted = Label(
    frame_middle,
    text="Desconto gerado",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
discountGenereted.place(
    x=150,
    y=220,
)

amount = Label(
    frame_middle,
    text="Quantidade de itens: ",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
amount.place(
    x=20,
    y=260,
)

amountGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
amountGenereted.place(
    x=150,
    y=260,
)
# labels / widget / buttons the right

dateCreate = Label(
    frame_middle,
    text="Data de criação",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
dateCreate.place(
    x=500,
    y=20,
)

dataCreateGenered = Label(
    frame_middle,
    text=f"{date_formated}",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
dataCreateGenered.place(
    x=680,
    y=20,
)

saller = Label(
    frame_middle,
    text="Vendedor",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
saller.place(
    x=500,
    y=60,
)

salesGenered = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
salesGenered.place(
    x=680,
    y=60,
)

formPayment = Label(
    frame_middle,
    text="Forma de pagamento",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
formPayment.place(
    x=500,
    y=100,
)

formPaymentGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
formPaymentGenereted.place(
    x=680,
    y=100,
)

subTotal = Label(
    frame_middle,
    text="Subtotal",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
subTotal.place(
    x=500,
    y=140,
)

subTotalGenereted = Label(
    frame_middle,
    text="XXXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
subTotalGenereted.place(
    x=680,
    y=140,
)

total = Label(
    frame_middle,
    text="Total",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
total.place(
    x=500,
    y=180,
)

totalGenereted = Label(
    frame_middle,
    text="XXXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
totalGenereted.place(
    x=680,
    y=180,
)

window.mainloop()
