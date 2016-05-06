'''
Created on 06.05.2016

@author: queaker
'''

import svgwrite

mmPerMHz = 3
mmPerBand = 20
sepBetweenBand = 40;

leftMargin = 100
topMargin = 10

if __name__ == '__main__':
    
    y = topMargin
    band = ''
    bandwidth = 0
    
    minFreq = 92233
    maxFreq = 0
    
    listOfChannels = []
    numberOfBands = 0;
    
    trimLow = 5360
    
    dwg = svgwrite.Drawing('band-and-channel-card.svg', profile='tiny')
    
    dwg.add(dwg.text('FPV Band and Channel Overview', (10, 32), fill='black', font_size="30px"))

    with open('channels.txt') as f:
        channels = [x.strip('\n') for x in f.readlines()]
        
        # find min/max
        for c in channels:
            
            # skip channel names
            if (len(c) < 3):
                continue
            
            elif (c.startswith('B')):
                numberOfBands +=1
                continue
            
            else:
                
                freq = int(c.split(' ')[1]);
                
                # remove odd freqencies
                if (freq < trimLow):
                    continue
                
                maxFreq = max(maxFreq, freq)
                minFreq = min(minFreq, freq)
                
                # save all channel frequencies
                if (freq not in listOfChannels):
                    listOfChannels.append(freq)
        
        # channel markers               
        #for c in listOfChannels:
        #    x = leftMargin + ((int(c) - minFreq) * mmPerMHz)
        #    dwg.add(dwg.rect((x - 1, 1), (1, (numberOfBands+1) * mmPerBand), fill='grey'))
        
        # draw all
        for c in channels:

            if (len(c) < 3):
                continue
            
            # new band
            if (c.startswith('B')):
                
                y = y + mmPerBand
                y = y + sepBetweenBand
                
                band = c.split(' ')[1]
                band = band.replace('_', ' ')
                bandwidth = int(c.split(' ')[2])
                
                # channel name
                dwg.add(dwg.text(band, (10, y), fill='black'))

                # line before band
                x = leftMargin + ((maxFreq - minFreq) * mmPerMHz + 30)
                dwg.add(dwg.line((0, y-20), (x, y-20), stroke=svgwrite.rgb(127, 127, 127)))
                
                continue
            
            # channel
            channelName = c.split(' ')[0]
            channelName = channelName.replace('_', ' ')
            freq = int(c.split(' ')[1])

            # remove odd freqencies
            if (freq < trimLow):
                continue
            
            posX = leftMargin + ((freq - minFreq) * mmPerMHz)
            posY = y
            
            # half size of red box
            bandwidthHalf = (bandwidth / 2) * mmPerMHz
            
            # red channel width
            #dwg.add(dwg.rect(               (posX - bandwidthHalf, posY), (bandwidthHalf*2, mmPerBand), fill='red'))
            
            # better polyline
            dwg.add(dwg.polyline([
                                    (posX - bandwidthHalf +5,       posY),            # LO
                                    (posX + bandwidthHalf -5,       posY),            # RO
                                    (posX + bandwidthHalf,          posY+mmPerBand),  # RU
                                    (posX - bandwidthHalf,          posY+mmPerBand)   # LU
                                ], fill='red'))



            
            # channel center marker
            dwg.add(dwg.rect(               (posX - 1, posY), (1, mmPerBand), fill='blue'))
            
            # channel description
            dwg.add(dwg.text(channelName,   (posX, posY), fill='blue'))
            
            # channel frequency
            dwg.add(dwg.text(freq,          (posX, posY + mmPerBand + 12), fill='blue'))
            

        
    dwg.save()



