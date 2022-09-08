# refer to https://gist.github.com/Potherca/18423260e2c9a4324c9ecb0c0a284066
#inputfile='/path/to/file.webm';
#outputfile="$(basename "${inputfile%.*}")";
#ffmpeg -i "${inputfile}" -pix_fmt rgb8 "${outputfile}.gif" \
#    && gifsicle --optimize=3 --output "${outputfile}-optimized.gif" --resize-height 600 "${outputfile}.gif"

import os
import sys
import getopt
import ffmpeg

def main(argv):
    inputfolder = ''
    gifsiclecheck = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:",["ifolder=","gifsicle="])
    except getopt.GetoptError:
        print('webm2gif.py -i <inputfolder> -s <gifsicle 0 or 1>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('webm2gif.py -i <inputfolder> -s <gifsicle 0 or 1>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputfolder = arg
        elif opt in ("-s", "--gifsicle"):
            gifsiclecheck = arg
    for dirpath, dirname, inputfilenames in os.walk(inputfolder):
        for inputfilename in inputfilenames:
            if (inputfilename.split(".")[1] == "gif") or (inputfilename.split(".")[1] == "GIF"):
                continue
            if (inputfilename.split(".")[1] == "webp") or (inputfilename.split(".")[1] == "WEBP") or (inputfilename.split(".")[1] == "webm") or (inputfilename.split(".")[1] == "WEBM"):
                gifpath = dirpath+"\\gif"
                if (not os.path.exists(gifpath)):
                    os.makedirs(gifpath)
                outputfilename = gifpath+"\\"+inputfilename.split(".")[0]+".gif"
                stream = ffmpeg.input(dirpath+"\\"+inputfilename)
                stream = ffmpeg.output(stream,outputfilename, pix_fmt='rgb8')
                stream.run(overwrite_output=True)
                if int(gifsiclecheck) > 0: 
                    gifsiclecommand = "gifsicle --optimize=3 --output "+"\""+outputfilename+"\""+" --resize-height 600 "+"\""+outputfilename+"\""
                    result = os.system(gifsiclecommand)
                    print(result)


if __name__ == "__main__":
   main(sys.argv[1:])