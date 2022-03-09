import requests
import glob

# import ipdb

url = "http://127.0.0.1:8000/invoices/uploadfiles"
# paths = glob.glob("/home/sung96kim/take-home/assets/*", recursive=True)
# # print(paths)
# files = [("files", open(path, "rb")) for path in paths]
files = [
    ("files", open("/home/sung96kim/take-home/assets/AriatInvoice03.28.19.pdf", "rb"))
]
print(files)
resp = requests.post(url=url, files=files)
print(resp.json())
print("Reached the end")

# ipdb.set_trace()
