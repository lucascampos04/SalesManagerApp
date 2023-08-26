from tkinter import (
    Button,
    Frame,
    Tk,
    messagebox,
    filedialog,
    Label,
    ttk,
    simpledialog,
)
from datetime import datetime

# colors
whitesmoke = "#dcdee8"
whiteBg = "#e6e7eb"
blackLight = "#3d3f47"
blackButLight = "#585959"
blue = "#213ac4"


# Logic
class SalesData:
    """Class to store sales data"""
    def __init__(self, id, valueFrete, date_creator, saller, form_pag, subTotal, total, amount):
        """Initialize an instance of the SalesData class"""
        self.id = id
        self.valueFrete = valueFrete
        self.date_creator = date_creator
        self.saller = saller
        self.form_pag = form_pag
        self.subTotal = subTotal
        self.total = total
        self.amount = amount

def get_inputs_users():
    """Get user input using dialog boxes"""
    id = simpledialog.askstring("Numero de serie do produto", "Numero do Produto: ")
    if (id is None):
        return None

    valueFrete = simpledialog.askfloat("Valor Frete", "Frete: ")
    if (valueFrete is None):
        return None

    date_creator = simpledialog.askstring("Data de entrega", "Data de entrega: ")
    if (date_creator is None):
        return None

    saller = simpledialog.askstring("Vendedor", "Vendedor")
    if (saller is None):
        return None

    form_pag = simpledialog.askstring("Forma de pagamento", "Forma de pagamento")
    if (form_pag is None):
        return None

    subTotal = simpledialog.askfloat("SubTotal", "SubTotal: ")
    if (subTotal is None):
        return None

    total = simpledialog.askfloat("Total", "Total: ")
    if (total is None):
        return None

    amount = simpledialog.askfloat("Quantidade", "Quantidade")
    if (amount is None):
        return None

    sales_data = SalesData(id, valueFrete, date_creator, saller, form_pag, subTotal, total, amount)
    return sales_data

def handleNew():
    """Handle creation of new sales and calculate discounts"""
    sales_data = get_inputs_users()

    if (sales_data is None):
        statusGenereted.config(text="Erro: Informações incorretas ou vazias.")
        return

    numberGenerated.config(text=sales_data.id)
    valueFreightGenereted.config(text=f"{sales_data.valueFrete}R$")
    amountGenereted.config(text=sales_data.amount)
    subTotalGenereted.config(text=sales_data.subTotal)
    totalGenereted.config(text=sales_data.total)

    # Value conversion
    freight_value = float(sales_data.valueFrete)
    subTotal_value = float(sales_data.subTotal)
    amount_value = float(sales_data.amount)

    discount_value = 0.0  # Defining a default value
    isDiscount_applied = False

    if (sales_data.total < 100):
        messagebox.showinfo("Desconto no frete", "Parabens voce ganhou 10% de desconto no frete.")
        newValueFreight = 30 - (30 * 0.30)
        valueFreightGenereted.config(text=f"{newValueFreight:.2f}R$")
        isDiscount_applied = True

    if (amount_value >= 4):
        messagebox.showinfo("Desconto","Parabens voce ganhou 10% de desconto. Na compra de mais 5 itens o desconto dobra.")
        newTotal = sales_data.total - (sales_data.total * 0.10)
        discount_value = 0.10
        totalGenereted.config(text=f"{newTotal:.2f}")
        subTotalGenereted.config(text=f"{newTotal:.2f}")
        discountGenereted.config(text=f"{discount_value * 100:.0f}%")
        isDiscount_applied = True

        if (isDiscount_applied):
            statusGenereted.config(text=f"Produto autorizado descontos")
            return
        else:
            statusGenereted.config(text=f"Produto autorizado com sucesso")

    return sales_data

    formatted_date = datetime.strptime(sales_data.date_creator, "%Y-%m-%d").strftime("%d/%m/%Y")
    dataCreateGenered.config(text=formatted_date)



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
    highlightthickness=2,
)
btn_save.place(
    x=79,
    y=10,
)

# buttons the right
btn_send = Button(
    frame_top,
    text="Emitir".upper(),
    font=("Arial 11 bold"),
    width=7,
    highlightbackground=blackLight,
    highlightthickness=2,
)
btn_send.place(
    x=310,
    y=10,
)

btn_quit = Button(
    frame_top,
    text="Cancelar".upper(),
    font=("Arial 11 bold"),
    highlightbackground=blackLight,
    highlightthickness=2,
)
btn_quit.place(
    x=390,
    y=10,
)

btn_sendEmail = Button(
    frame_top,
    text="Enviar por e-mail".upper(),
    font=("Arial 11 bold"),
    highlightbackground=blackLight,
    highlightthickness=2,
)
btn_sendEmail.place(
    x=493,
    y=10,
)

btn_search = Button(
    frame_top,
    text="Pesquisa".upper(),
    font=("Arial 11 bold"),
    highlightbackground=blackLight,
    highlightthickness=2,
)
btn_search.place(
    x=660,
    y=10,
)

# Front end middle

# labels / widget / buttons the left

number = Label(frame_middle, text="Número: ", font=("Arial 10 bold"), bg=whitesmoke)

number.place(
    x=20,
    y=20,
)

numberGenerated = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
numberGenerated.place(
    x=150,
    y=20,
)

status = Label(
    frame_middle,
    text="Status:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
status.place(
    x=20,
    y=60,
)

statusGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
statusGenereted.place(
    x=150,
    y=60,
)

client = Label(
    frame_middle,
    text="Cliente:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
client.place(
    x=20,
    y=100,
)

clientsOptions = ttk.Combobox(
    frame_middle,
    values=[
        "João",
        "Maria",
        "Pedro",
        "Ana",
        "Carlos",
        "Lúcia",
        "Miguel",
        "Isabela",
        "Rafael",
        "Sofia",
    ],
)
clientsOptions.place(
    x=150,
    y=100,
)

valueFreight = Label(
    frame_middle,
    text="Valor do frete:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
valueFreight.place(
    x=20,
    y=140,
)

valueFreightGenereted = Label(
    frame_middle,
    text="Frete gerado",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
valueFreightGenereted.place(
    x=150,
    y=140,
)

discount = Label(
    frame_middle,
    text="Valor Desconto:",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
discount.place(
    x=20,
    y=180,
)

discountGenereted = Label(
    frame_middle,
    text="Desconto gerado",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
discountGenereted.place(
    x=150,
    y=180,
)

amount = Label(
    frame_middle,
    text="Quantidade de itens: ",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
amount.place(
    x=20,
    y=220,
)

amountGenereted = Label(
    frame_middle,
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
amountGenereted.place(
    x=150,
    y=220,
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
    text="XXXXX",
    font=("Arial 10 bold"),
    bg=whitesmoke,
)
dataCreateGenered.place(
    x=650,
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

salesGenered = ttk.Combobox(
    frame_middle,
    values=[
        "Lucas",
        "João",
        "Lucas",
        "João",
        "Lucas",
        "João",
    ],
)
salesGenered.place(
    x=620,
    y=60,
)

saller = Label(
    frame_middle,
    text="Forma de pagamento",
    font=("Arial 8 bold"),
    bg=whitesmoke,
)
saller.place(
    x=500,
    y=100,
)

formPayment = ttk.Combobox(
    frame_middle,
    values=[
        "Cartão de debito",
        "Cartão de credito",
        "Boleto",
        "Pix",
    ],
)
formPayment.place(
    x=620,
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
    x=620,
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
    x=620,
    y=180,
)

window.mainloop()
