import requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import dateutil.relativedelta
import matplotlib.pyplot as plt


url_latest = "https://api.exchangeratesapi.io/latest?"
url_history = "https://api.exchangeratesapi.io/history?"

response = requests.get(url_latest)
rates = response.json()
currency_codes = list(rates['rates'].keys())
currency_codes.insert(0, 'EUR')
todays_date = datetime.date(datetime.now())
last_month = (todays_date + dateutil.relativedelta.relativedelta(months=-2))


def convert_currency(from_currency, to_currency, amount):
    params = {'symbols': from_currency+','+to_currency, 'base': from_currency}
    response = requests.get(url_latest, params=params)
    rates = response.json()
    fromC = round(rates['rates'][from_currency], 2)
    toC = round(rates['rates'][to_currency], 2)
    try:
        lbl_rate['text'] = format_rate(fromC, toC, from_currency, to_currency)
        lbl_value['text'] = calculate_value(toC, amount, to_currency)
    except:
        pass


def default():
    response = requests.get(url_latest)
    rates = response.json()
    return '1 EUR = ' + str(round(rates['rates']['USD'], 2)) + ' USD'


def calculate_value(toC, amount, to_currency):
    return (str(round(toC*float(amount), 2)) + ' ' + to_currency)


def format_rate(fromC, toC, fromSymbol, toSymbol):
    text_rate = (str(fromC), ' ', fromSymbol,
                 ' = ', str(toC), ' ', toSymbol)
    text_rate = ''.join(text_rate)
    return text_rate


def currency_history(from_currency, to_currency):
    params = {'base': from_currency, 'start_at': last_month,
              'end_at': todays_date}
    response = requests.get(url_history, params)
    rates = response.json()
    dates = list(rates['rates'].keys())
    day_price = []
    for x in range(len(dates)):
        day = str(dates[x])
        day_price.append(rates['rates'][day][to_currency])
    plot(dates, day_price)


def plot(dates, day_price):
    plt.plot(dates, day_price)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.xticks(rotation=90)
    plt.title('Last 2 Months Price Change')
    plt.show()


# create tkinter panel
root = tk.Tk()
root.title('Currency Converter')
root.geometry('300x350')

# hold all the elements
frame1 = tk.Frame(root, bd=1, relief='solid')
frame1.pack(fill=tk.BOTH, expand=True)
# show exchange rate
lbl_rate = tk.Label(frame1, text=default(), bd=1, relief='solid', font=('Courier', 8, 'bold'))
lbl_rate.place(relx=0.5, rely=0.08, relwidth=0.6, relheight=0.08, anchor=tk.N)
# show the value of the amount converted
lbl_value = tk.Label(frame1, text='Converter', font=(
    'Courier', 16, 'bold'), bd=1, relief='solid')
lbl_value.place(relx=0.5, rely=0.2, relwidth=0.85, relheight=0.15, anchor=tk.N)
# shows todays date
lbl_date = tk.Label(frame1, text=todays_date, font=('Courier',
                                                    8, 'bold'), bd=1, relief='solid')
lbl_date.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.1, anchor=tk.N)
# enter value amount to convert
lbl_amount = tk.Label(frame1, text='amount : ', bd=1, relief='solid')
lbl_amount.place(relx=0.28, rely=0.7, relwidth=0.4, relheight=0.1, anchor=tk.N)
amount_entry = tk.Entry(frame1, bd=1, relief='solid')
amount_entry.place(relx=0.68, rely=0.7, relwidth=0.5, relheight=0.1, anchor=tk.N)

# select base currency
lbl_to = tk.Label(frame1, text='from : ')
lbl_to.place(relx=0.14, rely=0.55, relheight=0.1, anchor=tk.N)
n = tk.StringVar()
from_select = ttk.Combobox(frame1, width=27, textvariable=n)
from_select['values'] = (currency_codes)
from_select.place(relx=0.36, rely=0.55, relwidth=0.3, relheight=0.1, anchor=tk.N)
from_select.current(0)
# select currency to convert to
lbl_to = tk.Label(frame1, text='to : ')
lbl_to.place(relx=0.58, rely=0.55, relheight=0.1, anchor=tk.N)
n = tk.StringVar()
to_select = ttk.Combobox(frame1, width=27, textvariable=n)
to_select['values'] = (currency_codes)
to_select.place(relx=0.78, rely=0.55, relwidth=0.3, relheight=0.1, anchor=tk.N)
to_select.current(0)


# button to view graph of rates changes
btnGraph = tk.Button(frame1, bd=1, relief='raised', bg='#c6c6cc', text='View Graph',
                     command=lambda: currency_history(from_select.get(), to_select.get()))
btnGraph.place(relx=0.68, rely=0.85, relwidth=0.3, relheight=0.08, anchor=tk.N)
# calculate new rate and value converted
btnConvert = tk.Button(frame1, bd=1, relief='raised', bg='#c6c6cc', text='Convert',
                       command=lambda: convert_currency(from_select.get(), to_select.get(), amount_entry.get()))
btnConvert.place(relx=0.32, rely=0.85, relwidth=0.3, relheight=0.08, anchor=tk.N)


root.mainloop()
