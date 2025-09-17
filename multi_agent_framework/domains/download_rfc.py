import requests

rfc_list = [1035, 2181, 8499, 4033, 4034, 4035, 7858, 8484, 9250, 6891]
for rfc in rfc_list:
    url = f"https://www.rfc-editor.org/rfc/rfc{rfc}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"rfc{rfc}.txt", "wb") as f:
            f.write(response.content)
        print(f"Downloaded RFC {rfc}")
    else:
        print(f"Failed to download RFC {rfc}")
