import sys
import requests;

def main():
    urls = sys.argv[1:]
    with open('output_file', 'w') as file:
        for url in urls:
            try:
                response = requests.get(url)
                response_code = response.status_code
                if response_code in [200, 403]:
                    file.write(f'Status code - {response_code} : {url}\n')
            except requests.RequestException as e:
                print(f'Error {url} : {e}\n')
                return

if __name__=='__main__':
    main()

