
from configparser import ConfigParser
from pprint import pprint
from aip import AipOcr
from PIL.ImageGrab import grabclipboard


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def ocr_baidu(client,image):
    options = {
                "language_type":"CHN_ENG",
                "detect_direction":"true",
                "detect_language":"true",
                "probability":"true"
                }
    result = client.basicAccurate(image, options)
    # pprint(result)
    try:
        txtlist = [ x['words'] for x in result['words_result'] ]
    # pprint(txt)
    except:
        errcode = result['error_code']
        err = result['error_msg']
        raise SystemExit(errcode,err)
    return txtlist


def murge_txt(txtlist:list):
    baselen = max(len(x) for x in txtlist)-4
    output = []
    tmpstr = ''
    for x in txtlist:
        if len(x) < baselen and tmpstr != '':
            output.append(tmpstr)
            tmpstr = ''
            output.append(x)
        elif len(x) < baselen and tmpstr == '':
            output.append(x)
        elif len(x) >= baselen :
            tmpstr += x
    return output


def main(murge=True,pic=None):
   
    confile = r'M:\GH\_pri\baidu.ini'
    config = ConfigParser()
    config.read(confile)
    APP_ID = config.get('BaiduOcr','APP_ID') 
    API_KEY = config.get('BaiduOcr','API_KEY')
    SECRET_KEY = config.get('BaiduOcr','SECRET_KEY')
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    if pic:
        img = get_file_content(pic)
    else:
        img = grabclipboard()
    img.save('tmp.png', 'PNG')
    data = get_file_content('tmp.png')
    txtlist = ocr_baidu(client,data)
    if murge:
        txtlist = murge_txt(txtlist)
    for x in txtlist:
        print(x)

if __name__ == "__main__":
    main(murge=True)