const http = require('http');
const request = require('request');
//const spawn = require("child_process");
//const WHDH = 'C:\\Program Files (x86)\\ARM Software\\MacroMaker\\WHDH.bat';

//var shell = new ActiveXObject('WScript.Shell');

 
console.log('Server Running...');

const requestListener = function (req, res) {
  let channels = ['stopWHDH','WHDH','stopFOX','FOX','stopCBS','CBS','stopCW','CW','stopNBC','NBC','stopUnimas','Unimas','stopABC','ABC','stopTelemundo','Telemundo','stopUnivision','Univision','stopION','ION'];
  console.log('End Point Requested is ' + req.url.slice(1,))



  for (let index = 0; index < 4; index++) {
    
    request('http://192.168.1.66/tuners.html?page=tuner' + index, function (
        error,
        response,
        body
      ) {
        //console.error('error:', error)
        //console.log(body.split('Resource Lock</td><td>')[1].split('</td>')[0])
        var TunerStatus = body.split('Resource Lock</td><td>')[1].split('</td>')[0]
        console.log(`Tuner ${index}  status is "${TunerStatus}"`)
        if (TunerStatus == "192.168.1.98") {
            console.log('getting virtual channel name')
            var ChannelStream = body.split('Virtual Channel</td><td>')[1].split('</td></tr>')[0];
            console.log(ChannelStream);
            RawChan = ['7.1 WHDH','25.1 WFXT','4.1 WBZ-DT','56.1 WLVI','15.1 WBTS-CD','27.1 UniMas','5.1 WCVB','60.1 WNEU-DT','66.1 WUNI-DT','68.1 ION']
            ChannelsCuteNames = ['WHDH','FOX','CBS','CW','NBC','Unimas','ABC','Telemundo','Univision','ION']
            console.log(RawChan.length)
            console.log(ChannelsCuteNames.length)
            for (let y = 0; y < RawChan.length; y++) {
               if (ChannelStream == RawChan[y]){
                    console.log('match found = ' + RawChan[y])
                    console.log('Variable y = ' + y)
                    console.log('Channel Cute Name = ' + ChannelsCuteNames[y])
                    try {
                        for (let x = 0; x < channels.length ; x++) {
                        if (req.url.slice(1,) == channels[x]) {
                            console.log("Activating Stream")
                            res.writeHead(200,  {'Content-Type': 'text/html'});
                          
                            res.write('Activating the ' + req.url.slice(1,) + ' Channel shortcut.'); //web browser text
                            res.end();
                            break;
                        }
                        
                        else if (req.url.slice(1,) != channels[x]) {
                            console.log("Activating Stream")
                            res.writeHead(200,  {'Content-Type': 'text/html'});
                            //require('child_process').exec('cmd /c \"C:\\Program Files (x86)\\ARM Software\\MacroMaker\\' + req.url.slice(1,) + '.lnk\"', function(){}); //line of code for MediaPC only
                            res.write('Activating the ' + req.url.slice(1,) + ' Channel shortcut.'); //web browser text
                            res.end();
                            break;
                        } 
                        
                        else if (x == channels.length - 1) {
                          res.writeHead(404,  {'Content-Type': 'text/html'});
                          res.write('ERROR 404, Page Not Found.');
                          res.end(); //USE
                          break;
                              }
                          }
                      } catch (error) {}
               }
            }
        }
      }) 
    }
}


const server = http.createServer(requestListener);
server.listen(8282);
